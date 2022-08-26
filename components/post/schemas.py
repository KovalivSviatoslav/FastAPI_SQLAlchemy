import datetime
from typing import List, Optional

from pydantic import BaseModel

from components.comment.schemas import CommentDetailResponse
from components.post.models import BasePost


class PostCreateUpdateBody(BasePost):
    category: str


class CategorySchema(BaseModel):
    name: str


class PostCreateUpdateResponse(BasePost):
    id: int
    avg_rating: Optional[int]
    created_at: datetime.datetime
    category: CategorySchema


class PostDetailUpdateResponse(PostCreateUpdateResponse):
    comments: List[CommentDetailResponse]
