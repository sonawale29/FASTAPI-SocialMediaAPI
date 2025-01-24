from sqlalchemy import Column, String,Integer,Text,ForeignKey,DateTime
from .database import Base
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func


# User Table Model
class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    posts = relationship("PostModel", back_populates="author")
    likes = relationship("LikeModel", back_populates="user", cascade="all, delete")
    comments = relationship("CommentModel", back_populates="user", cascade="all, delete")


class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    author_id = Column(String, ForeignKey("users.id"))
    author = relationship("UserModel", back_populates="posts")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    likes = relationship("LikeModel", back_populates="post", cascade="all, delete")
    comments = relationship("CommentModel", back_populates="post", cascade="all, delete")


class LikeModel(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserModel", back_populates="likes")
    post = relationship("PostModel", back_populates="likes")


class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("UserModel", back_populates="comments")
    post = relationship("PostModel", back_populates="comments")

