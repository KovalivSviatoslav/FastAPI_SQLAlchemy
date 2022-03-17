import datetime

from components.comment.models import BaseComment
from components.user.schemas import UserDetailSchema


class CommentCreateBody(BaseComment):
    post_id: int


class CommentDetailResponse(BaseComment):
    id: int
    created_at: datetime.datetime
    user: UserDetailSchema


class CommentUpdateBody(BaseComment):
    pass
