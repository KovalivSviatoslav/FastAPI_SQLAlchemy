from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from components.comment.models import Comment


class CommentService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: dict, user_id: int) -> Comment:
        comment = Comment(**data, user_id=user_id)
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def delete(self, comment_id: int) -> None:
        comment = await self._session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment does not exists.")

        await self._session.delete(comment)
        await self._session.commit()

    async def update(self, comment_id: int, data: dict) -> Comment:
        comment = await self._session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment does not exists.")

        for key, value in data.items():
            setattr(comment, key, value)

        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment
