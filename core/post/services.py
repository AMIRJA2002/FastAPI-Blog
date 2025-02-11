from core.post.schemas import AddComment, CreateUpdatePost, SuccessResponse
from sqlalchemy.dialects.postgresql import insert
from core.post.models import Post, Tag, Comment
from sqlalchemy.ext.asyncio import AsyncSession
from core.users.models import User, Role
from sqlalchemy.orm import joinedload
from sqlalchemy import select, delete
from fastapi import HTTPException
from sqlalchemy import or_, func
from .models import PostTag
from datetime import date
from typing import List


class PostService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, post_data: CreateUpdatePost, user: User) -> Post:
        if user.role not in [Role.admin, Role.author]:
            raise HTTPException(status_code=403, detail="You do not have permission for this action")

        post = Post(title=post_data.title, content=post_data.content, author_id=user.id)
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)

        query = select(Tag).where(Tag.name.in_(post_data.tags))
        result = await self.db.execute(query)
        tags = result.scalars().all()
        post_tag_list = [PostTag(post_id=post.id, tags_id=tag.id) for tag in tags]
        self.db.add_all(post_tag_list)
        await self.db.commit()

        return post

    async def update(self, post_data: CreateUpdatePost, post: Post) -> Post:
        post.title = post_data.title
        post.content = post_data.content

        query = select(Tag).where(Tag.name.in_(post_data.tags))
        result = await self.db.execute(query)
        tags = result.scalars().all()
        post_tag_list = [PostTag(post_id=post.id, tags_id=tag.id) for tag in tags]
        self.db.add_all(post_tag_list)
        await self.db.commit()

        return post

    async def delete(self, post: Post) -> SuccessResponse:
        query = select(Post).where(Post.id == post.id).options(joinedload(Post.tags), joinedload(Post.post_comments))
        result = await self.db.execute(query)
        post = result.unique().scalars().first()
        post_id = post.id
        await self.db.execute(delete(Comment).where(Comment.post_id == post_id))

        await self.db.execute(delete(PostTag).where(PostTag.post_id == post_id))
        await self.db.delete(post)
        await self.db.commit()

        return SuccessResponse(
            message="Post deleted successfully!",
            data={"post_id": post_id}
        )

    async def get_by_filter(self, date: date | None, tags: List[str], keyword: str | None, author: str | None):
        query = select(Post).options(joinedload(Post.tags), joinedload(Post.author))

        if date:
            query = query.where(Post.date <= date)

        if tags:
            query = query.where(Post.tags.any(Tag.name.in_(tags)))

        if keyword:
            query = query.filter(or_(
                func.lower(Post.title).like(f"%{keyword.lower()}%"),
                func.lower(Post.content).like(f"%{keyword.lower()}%")
            ))

        if author:
            query = query.where(func.lower(User.username) == author.lower())

        return query

    async def get(self, post_id: int):
        query = select(Post).options(joinedload(Post.tags)).where(Post.id == post_id)
        result = await self.db.execute(query)
        post = result.unique().scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        return post


class CommentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, comment_data: AddComment, user: User) -> Comment:
        query = select(Post.id).where(Post.id == comment_data.post_id)
        post = await self.db.scalar(query)
        if not post:
            raise HTTPException(status_code=404, detail='post not found')

        comment = Comment(content=comment_data.content, user_id=user.id, post_id=comment_data.post_id)
        self.db.add(comment)
        await self.db.commit()
        return comment

    async def get(self, post_id: int, user: User):
        query = select(Post).options(joinedload(Post.post_comments)).filter(Post.id == post_id)
        result = await self.db.execute(query)
        post = result.unique().scalar()
        if not post:
            raise HTTPException(status_code=404, detail='post not found')

        if user.role == Role.admin or user.id == post.author.id:
            return post

        raise HTTPException(status_code=403, detail='You do not have permission for this action')

    async def delete(self, post_id: int, comment_id: int, user: User) -> SuccessResponse:
        if not user.role == Role.admin:
            raise HTTPException(status_code=403, detail='you do not have permission for this action')

        query = select(Post).where(Post.id == post_id)
        result = await self.db.execute(query)
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail='post not found')

        query = select(Comment).where(Comment.id == comment_id, Comment.post_id == post.id)
        result = await self.db.execute(query)
        comment = result.scalar_one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail='comment not found')

        comment_id = comment.id
        await self.db.delete(comment)
        await self.db.commit()

        return SuccessResponse(
            message="comment deleted successfully!",
            data={"comment_id": comment_id}
        )


async def create_tag_service(tags: List[str], db: AsyncSession) -> None:
    query = insert(Tag).values([{'name': tag} for tag in tags])
    query = query.on_conflict_do_nothing(index_elements=['name'])
    await db.execute(query)
    await db.commit()


async def get_all_tags(db: AsyncSession) -> dict[str, list]:
    query = select(Tag)
    result = await db.execute(query)
    tags = result.scalars().all()

    return {
        'tags': [tag.__dict__ for tag in tags]
    }
