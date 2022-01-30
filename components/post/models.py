from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from components.user.models import User
from db.config import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, back_populates="posts")


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, back_populates="ratings")
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post, back_populates="ratings")
