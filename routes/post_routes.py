from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import SessionLocal
from db.models import PostModel,CommentModel,LikeModel
from schemas.posts_schema import *
from sqlalchemy.exc import IntegrityError
from dependencies import get_current_user


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize router
post_router = APIRouter()


# CRUD Endpoints
@post_router.post("/posts/", response_model=PostOut, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    db_post = PostModel(**post.dict())
    try:
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except IntegrityError:  # Handle cases where author_id doesn't exist
        db.rollback()  # Rollback the changes to avoid database inconsistency
        raise HTTPException(status_code=400, detail="Author with provided ID does not exist")


@post_router.get("/posts/", response_model=List[PostOut])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               current_user: dict = Depends(get_current_user)):
    posts = db.query(PostModel).offset(skip).limit(limit).all()
    return posts


@post_router.get("/posts/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@post_router.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.dict(exclude_unset=True).items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


@post_router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return None

@post_router.post("/posts/{post_id}/like")
def like_post(post_id: int, user_id: str, db: Session = Depends(get_db)):
    # Check if post exists
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user has already liked the post
    existing_like = db.query(LikeModel).filter(
        LikeModel.post_id == post_id, LikeModel.user_id == user_id
    ).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked")

    # Add the like
    new_like = LikeModel(post_id=post_id, user_id=user_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return {"message": "Post liked successfully"}


# Add a comment
@post_router.post("/posts/{post_id}/comments")
def add_comment(post_id: int, comment: CommentRequest, user_id: str, db: Session = Depends(get_db)):
    # Check if post exists
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Add the comment
    new_comment = CommentModel(post_id=post_id, user_id=user_id, content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"message": "Comment added successfully", "comment": comment.content}
