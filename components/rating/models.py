from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from pydantic import conint

from components.post.models import Post
from components.user.models import User


class BaseRating(SQLModel):
    value: conint(ge=1, le=10)


class Rating(BaseRating, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="ratings")
    post_id: Optional[int] = Field(default=None, foreign_key="post.id")
    post: Optional[Post] = Relationship(back_populates="ratings")
