from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from core.users.models import User
from asyncdatabase import Base


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    author: Mapped["User"] = relationship("User", backref="posts")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary='post_tag', back_populates="posts")
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    posts: Mapped["Post"] = relationship('Post', secondary='post_tag', backref='post_tags')


class PostTag(Base):
    __tablename__ = 'post_tag'

    id = Column(Integer, index=True, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id', ondelete='CASCADE'))
    tags_id: Mapped[int] = mapped_column(Integer, ForeignKey('tag.id', ondelete='CASCADE'))


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship('User', backref='user_comments')
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id', ondelete='CASCADE'))
    post: Mapped['Post'] = relationship('Post', backref='post_comments')
