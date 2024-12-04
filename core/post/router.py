from typing import Optional
from fastapi import Query
from dependencies import get_db, get_current_user
from .dependency import post_permission
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.users.models import User
from .models import Post
from .schemas import (
    CreateUpdatePost,
    CreateTag,
    AddComment,
    PostCommentsResponse,
    PostPaginatedResponse,
)
from .services import (
    get_all_posts,
    get_post_by_id,
    create_tag_service,
    get_all_tags,
    create_post_service,
    edit_post_service,
    delete_post_service,
    add_comment_service,
    comments_list_service,
    delete_comment_service,
)

post_router = APIRouter()


@post_router.post('/create')
def create_post(post_data: CreateUpdatePost, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_post_service(post_data, user, db)


@post_router.get('/list', response_model=PostPaginatedResponse)
def list_post(page: int = 1, date: Optional[str] = None, tags: Optional[list[str]] = Query(default=[]),
              keyword: Optional[str] = None,
              author: Optional[str] = None, db: Session = Depends(get_db)):
    return get_all_posts(page, date, tags, keyword, author, db)


@post_router.get('/{post_id}')
def view_post(post_id: str, db: Session = Depends(get_db)):
    return get_post_by_id(post_id, db)


@post_router.put('/update/{post_id}')
def edit_post(post_data: CreateUpdatePost, db: Session = Depends(get_db), post: Post = Depends(post_permission)):
    return edit_post_service(post_data, db, post)


@post_router.delete('/delete/{post_id}')
def delete_post(db: Session = Depends(get_db), post: Post = Depends(post_permission)):
    return delete_post_service(db, post)


@post_router.post('/comment/add')
def add_comment(comment_data: AddComment, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return add_comment_service(comment_data, db, user)


@post_router.get('/comments/{post_id}', response_model=PostCommentsResponse)
def post_comments_list(post_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return comments_list_service(post_id, db, user)


@post_router.get('/comment/delete/{post_id}/{comment_id}')
def delete_comment(post_id: str, comment_id: str, db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    return delete_comment_service(post_id, comment_id, db, user)


@post_router.post('/tags/create')
def create_tag(tag_data: CreateTag, db: Session = Depends(get_db)):
    return create_tag_service(tag_data, db)


@post_router.get('/tags/list')
def list_tags(db: Session = Depends(get_db)):
    return get_all_tags(db)
