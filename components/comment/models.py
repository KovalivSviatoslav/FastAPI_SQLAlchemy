from datetime import datetime

from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from components.post.models import Post
from components.user.models import User
from db.config import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
    is_updated = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, back_populates="comments")
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post, back_populates="comments")
