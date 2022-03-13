import datetime

from components.comment.models import BaseComment
from components.user.schemas import UserDetailSchema


class CommentCreateSchema(BaseComment):
    post_id: int


class CommentDetailSchema(BaseComment):
    id: int
    created_at: datetime.datetime
    user: UserDetailSchema
