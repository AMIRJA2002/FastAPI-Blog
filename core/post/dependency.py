from dependencies import get_current_user, aget_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from core.users.models import User, Role
from sqlalchemy import select
from .models import Post


async def post_permission(post_id: int, db: AsyncSession = Depends(aget_db), user: User = Depends(get_current_user)):
    query = select(Post).where(Post.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail='post not found')
    if post.author_id == user.id or user.role == Role.admin:
        return post

    raise HTTPException(status_code=403, detail='You do not have permission for this action')
