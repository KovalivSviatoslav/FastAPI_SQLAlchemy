import datetime
from typing import Optional

from sqlalchemy import DateTime, Column, Text
from sqlmodel import SQLModel, Field, Relationship

from components.post.models import Post
from components.user.models import User


class BaseComment(SQLModel):
    message: str = Field(
        sa_column=Column(Text, nullable=False)
    )


class Comment(BaseComment, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_updated: Optional[bool] = Field(default=False)
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime, default=datetime.datetime.now)
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime, onupdate=datetime.datetime.now)
    )
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="comments")
    post_id: Optional[int] = Field(default=None, foreign_key="post.id")
    post: Optional[Post] = Relationship(back_populates="comments")
