from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str
    lastname: str
    email: str = Field(sa_column_kwargs={"unique": True})
    password: str
    # backward relationship
    posts: List["Post"] = Relationship(back_populates="user")
    ratings: List["Rating"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")
