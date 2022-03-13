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
