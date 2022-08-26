import datetime
from typing import Optional, List, TYPE_CHECKING

from pydantic import conint
from sqlalchemy import DateTime, Column, Text
from sqlmodel import SQLModel, Field, Relationship

from components.user.models import User

if TYPE_CHECKING:
    from components.comment.models import Comment
    from components.rating.models import Rating


class BasePost(SQLModel):
    name: str = Field(sa_column_kwargs={"unique": True})
    body: str = Field(
        sa_column=Column(Text, nullable=False)
    )


class Post(BasePost, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime, default=datetime.datetime.now)
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime, onupdate=datetime.datetime.now)
    )
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="posts")
    # backward relationship
    ratings: List["Rating"] = Relationship(back_populates="post")
    comments: List["Comment"] = Relationship(back_populates="post")

    # rating calculated by task
    avg_rating: Optional[conint(ge=1, le=10)]


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True})
    # backward relationship
    posts: List["Post"] = Relationship(back_populates="category")
