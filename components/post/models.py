import datetime
from typing import Optional, List

from sqlalchemy import DateTime, Column, Text
from sqlmodel import SQLModel, Field, Relationship

from components.user.models import User


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
    # backward relationship
    ratings: List["Rating"] = Relationship(back_populates="post")
    comments: List["Comment"] = Relationship(back_populates="post")


class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="ratings")
    post_id: Optional[int] = Field(default=None, foreign_key="post.id")
    post: Optional[Post] = Relationship(back_populates="ratings")
