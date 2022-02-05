from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from components.user.models import User
from components.user.services import UserService
from config.app import AppConfig
from config.db import get_session


class AuthHandler:

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = AppConfig().jwt_secret

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=AppConfig().access_token_expire_minutes),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=AppConfig().jwt_algorithm
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    async def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security),
                               session: AsyncSession = Depends(get_session)) -> User:
        user_id = self.decode_token(auth.credentials)
        user = await UserService(session).get_user_by_id(user_id)
        return user
