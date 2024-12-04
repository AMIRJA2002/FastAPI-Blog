from dependencies import get_db, get_current_user
from fastapi import HTTPException, Depends
from core.users.models import User, Role
from sqlalchemy.orm import Session
from .models import Post


def post_permission(post_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail='post not found')
    if post.author.id == user.id or user.role == Role.admin:
        return post

    raise HTTPException(status_code=403, detail='You do not have permission for this action')
