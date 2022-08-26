from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from components.post.models import Post
    from components.comment.models import Comment
    from components.rating.models import Rating


class BaseUser(SQLModel):
    firstname: str
    lastname: str
    email: str = Field(sa_column_kwargs={"unique": True})


class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    # backward relationship
    posts: List["Post"] = Relationship(back_populates="user")
    ratings: List["Rating"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")
