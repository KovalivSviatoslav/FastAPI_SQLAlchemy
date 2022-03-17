import datetime
from typing import List

from components.comment.schemas import CommentDetailSchema
from components.post.models import BasePost


class PostCreateUpdateBody(BasePost):
    pass


class PostCreateUpdateResponse(BasePost):
    id: int
    created_at: datetime.datetime


class PostDetailUpdateResponse(PostCreateUpdateResponse):
    comments: List[CommentDetailSchema]
