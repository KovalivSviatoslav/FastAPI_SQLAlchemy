import datetime
from typing import List, Optional

from components.comment.schemas import CommentDetailResponse
from components.post.models import BasePost


class PostCreateUpdateBody(BasePost):
    pass


class PostCreateUpdateResponse(BasePost):
    id: int
    avg_rating: Optional[int]
    created_at: datetime.datetime


class PostDetailUpdateResponse(PostCreateUpdateResponse):
    comments: List[CommentDetailResponse]
