from core.post.models import Post, Tag, Comment
from sqlalchemy.orm import Session, joinedload
from core.users.models import User, Role
from .paginator import paginate_query
from sqlalchemy.sql import exists
from fastapi import HTTPException
from sqlalchemy import or_, func
from datetime import datetime
from .models import PostTag
from typing import List
from core.post.schemas import (
    CreateTag,
    CreateUpdatePost,
    AddComment,
    PostCommentsResponse,
)


def create_post_service(post_data: CreateUpdatePost, user: User, db: Session) -> dict[str, CreateUpdatePost]:
    if not user.role in [Role.admin, Role.author]:
        raise HTTPException(status_code=403, detail='you do not have permission for this action')

    post = Post(title=post_data.title, content=post_data.content, author_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)

    post_tags = []
    for tag_name in post_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if tag:
            new_post_tag = PostTag(post_id=post.id, tags_id=tag.id)
            post_tags.append(new_post_tag)

    db.bulk_save_objects(post_tags)
    db.commit()

    return CreateUpdatePost(
        title=post.title,
        content=post.content,
        tags=[tag.name for tag in post.tags]
    )


def edit_post_service(post_data: CreateUpdatePost, db: Session, post: Post) -> dict:
    post.title = post_data.title
    post.content = post_data.content

    post_tags = []
    for tag_name in post_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if tag:
            new_post_tag = PostTag(post_id=post.id, tags_id=tag.id)
            post_tags.append(new_post_tag)

    if post_tags:
        db.query(PostTag).filter(PostTag.post_id == post.id).delete()
        db.bulk_save_objects(post_tags)

    db.commit()

    return CreateUpdatePost(
        title=post.title,
        content=post.content,
        tags=[tag.name for tag in post.tags]
    )


def delete_post_service(db: Session, post: Post) -> dict:
    db.delete(post)

    db.commit()

    return {
        'data': 'post deleted!'
    }


def get_all_posts(page: int, date: str | None, tags: List[str] | [], keyword: str | None, author: str | None,
                  db: Session):
    query = db.query(Post).options(joinedload(Post.tags), joinedload(Post.author))

    if date:
        try:
            date = datetime.fromisoformat(date)
        except:
            raise HTTPException(status_code=400, detail='wrong date format')

        query = query.filter(Post.date <= date)

    if tags:
        query = query.filter(Post.tags.any(Tag.name.in_(tags)))

    if keyword:
        query = query.filter(or_(
            func.lower(Post.title).like(f"%{keyword.lower()}%"),
            func.lower(Post.content).like(f"%{keyword.lower()}%")
        ))

    if author:
        print(author)
        query = query.filter(func.lower(User.username) == author.lower())

    return paginate_query(query, page)


def get_post_by_id(post_id: str, db: Session) -> dict[str, dict[str, list]]:
    post = db.query(Post).options(joinedload(Post.tags)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    return {
        'post': {
            **post.__dict__,
            'tags': [tag.name for tag in post.tags]
        }
    }


def add_comment_service(comment_data: AddComment, db: Session, user: User) -> AddComment:
    post = db.query(exists().where(Post.id == comment_data.post_id)).scalar()
    if not post:
        raise HTTPException(status_code=404, detail='post not found')

    comment = Comment(content=comment_data.content, user_id=user.id, post_id=comment_data.post_id)
    db.add(comment)
    db.commit()
    return AddComment(content=comment.content, post_id=comment.post_id)


def comments_list_service(post_id: str, db: Session, user: User) -> PostCommentsResponse:
    post = db.query(Post).options(joinedload(Post.comments)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail='post not found')

    if user.role.value == Role.admin.value or user.id == post.author.id:
        return post

    raise HTTPException(status_code=403, detail='You do not have permission for this action')


def delete_comment_service(post_id: str, comment_id: str, db: Session, user: User) -> dict:
    if not user.role == Role.admin:
        raise HTTPException(status_code=403, detail='you do not have permission for this action')

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail='post not found')

    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail='comment not found')

    db.delete(comment)
    db.commit()

    return {
        'data': 'comment deleted'
    }


def create_tag_service(tag_data: CreateTag, db: Session) -> dict[str, str]:
    tag = Tag(name=tag_data.name),
    db.add(tag), db.commit()
    return {
        'message': 'tag created'
    }


def get_all_tags(db: Session) -> dict[str, list]:
    tags = db.query(Tag).all()
    return {
        'tags': [tag.__dict__ for tag in tags]
    }
