from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class BaseUser(SQLModel):
    firstname: str
    lastname: str
    email: str = Field(sa_column_kwargs={"unique": True})


class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str

    posts: List["Post"] = Relationship(back_populates="user")
    ratings: List["Rating"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")
