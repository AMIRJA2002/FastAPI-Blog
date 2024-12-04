from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime


class CreateUpdatePost(BaseModel):
    title: str
    content: str
    tags: List[str] | None = []


class AddComment(BaseModel):
    content: str
    post_id: int


class CommentResponse(BaseModel):
    content: str
    user_id: int

    class Config:
        orm_mode = True


class PostCommentsResponse(BaseModel):
    title: str
    content: str
    comments: List[CommentResponse]

    class Config:
        orm_mode = True


class TagSchema(BaseModel):
    name: str


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    date: Optional[datetime] = None
    tags: List[str]

    @validator('tags', pre=True)
    def convert_tags(cls, v):
        if isinstance(v, list):
            return [tag.name for tag in v]
        return v

    class Config:
        orm_mode = True


class PostPaginatedResponse(BaseModel):
    results: List[PostSchema]
    page: int
    page_size: int
    total_results: int
    total_pages: int

    class Config:
        orm_mode = True


class CreateTag(BaseModel):
    name: str
