from pydantic import BaseModel, field_validator
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
    id: int
    user_id: int
    post_id: int
    content: str

    class Config:
        from_attributes = True


class PostCommentsResponse(BaseModel):
    id: int
    title: str
    content: str
    date: datetime
    post_comments: List[CommentResponse]

    class Config:
        from_attributes = True


class TagSchema(BaseModel):
    name: str


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    date: Optional[datetime] = None
    tags: List[str]

    @field_validator('tags', mode='before')
    def convert_tags(cls, v):
        if isinstance(v, list):
            return [tag.name for tag in v]
        return v

    class Config:
        from_attributes = True


class PostPaginatedResponse(BaseModel):
    results: List[PostSchema]
    page: int
    page_size: int
    total_results: int
    total_pages: int

    class Config:
        from_attributes = True


class CreateTag(BaseModel):
    name: str


class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    data: dict | None = None