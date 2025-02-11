from .services import PostService, CommentService, create_tag_service, get_all_tags
from dependencies import get_current_user, aget_db
from sqlalchemy.ext.asyncio import AsyncSession
from .dependency import post_permission
from fastapi import APIRouter, Depends
from .paginator import paginate_query
from core.users.models import User
from typing import Optional
from datetime import date
from fastapi import Query
from .models import Post
from .schemas import (
    CreateUpdatePost,
    CreateTag,
    AddComment,
    PostCommentsResponse,
    PostPaginatedResponse,
    CommentResponse,
    PostSchema,
    SuccessResponse,
)

post_router = APIRouter()


@post_router.post('', response_model=PostSchema)
async def create_post(post_data: CreateUpdatePost, db: AsyncSession = Depends(aget_db),
                      user: User = Depends(get_current_user)):
    if post_data.tags:
        await create_tag_service(post_data.tags, db)
    post_service = PostService(db)
    post = await post_service.create(post_data, user)
    return await post_service.get(post.id)


@post_router.get('', response_model=PostPaginatedResponse)
async def list_post(page: int = 1, date: Optional[date] = None, tags: Optional[list[str]] = Query(default=[]),
                    keyword: Optional[str] = None, author: Optional[str] = None, db: AsyncSession = Depends(aget_db)):
    result = await PostService(db).get_by_filter(date, tags, keyword, author)
    return await paginate_query(result, db, page)


@post_router.get('/{post_id}', response_model=PostSchema)
async def get_post(post_id: int, db: AsyncSession = Depends(aget_db)):
    return await PostService(db).get(post_id)


@post_router.put('/{post_id}', response_model=PostSchema)
async def update_post(post_data: CreateUpdatePost, db: AsyncSession = Depends(aget_db),
                      post: Post = Depends(post_permission)):
    if post_data.tags:
        await create_tag_service(post_data.tags, db)
    post_service = PostService(db)
    post = await post_service.update(post_data, post)
    return await post_service.get(post.id)


@post_router.delete('/{post_id}', response_model=SuccessResponse)
async def delete_post(db: AsyncSession = Depends(aget_db), post: Post = Depends(post_permission)):
    return await PostService(db).delete(post)


@post_router.post('/comment', response_model=CommentResponse)
async def add_comment(comment_data: AddComment, db: AsyncSession = Depends(aget_db),
                      user: User = Depends(get_current_user)):
    return await CommentService(db).create(comment_data, user)


@post_router.get('/comment/{post_id}', response_model=PostCommentsResponse)
async def post_comments_list(post_id: int, db: AsyncSession = Depends(aget_db), user: User = Depends(get_current_user)):
    return await CommentService(db).get(post_id, user)


@post_router.delete('/comment/{post_id}/{comment_id}', response_model=SuccessResponse)
async def delete_comment(post_id: int, comment_id: int, db: AsyncSession = Depends(aget_db),
                         user: User = Depends(get_current_user)):
    return await CommentService(db).delete(post_id, comment_id, user)


@post_router.post('/tags/create')
async def create_tag(tag_data: CreateTag, db: AsyncSession = Depends(aget_db)):
    return await create_tag_service(tag_data, db)


@post_router.get('/tags/list')
async def list_tags(db: AsyncSession = Depends(aget_db)):
    return await get_all_tags(db)
