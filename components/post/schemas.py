import datetime
from typing import List

from components.comment.schemas import CommentDetailSchema
from components.post.models import BasePost


class PostCreateBody(BasePost):
    pass


class PostCreateResponse(BasePost):
    id: int
    created_at: datetime.datetime


class PostDetailResponse(PostCreateResponse):
    comments: List[CommentDetailSchema]
