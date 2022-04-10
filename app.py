from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from components.post.services import PostService
from config.db import engine
from config.app import AppConfig
from components.user.views import user_router
from components.post.views import post_router
from components.comment.views import comment_router
from components.rating.views import rating_router
from components.user.models import User
from components.post.models import Post
from components.comment.models import Comment
from components.rating.models import Rating


app = FastAPI(title=AppConfig().title, version=AppConfig().version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=AppConfig().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(rating_router)


@app.on_event("startup")
@repeat_every(seconds=60, wait_first=True, raise_exceptions=True)
async def calculate_ratings() -> None:
    async with AsyncSession(engine) as session:
        await PostService(session).calculate_ratings()
