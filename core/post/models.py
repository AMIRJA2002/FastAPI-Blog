from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from datebase import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', backref='posts')
    tags = relationship('Tag', secondary='post_tag', backref='tags')
    date = Column(DateTime, default=datetime.utcnow)


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    posts = relationship('Post', secondary='post_tag', backref='posts')


class PostTag(Base):
    __tablename__ = 'post_tag'

    id = Column(Integer, index=True, primary_key=True)
    post_id = Column('post_id', Integer, ForeignKey('post.id', ondelete='RESTRICT'))
    tags_id = Column('tags_id', Integer, ForeignKey('tag.id', ondelete='RESTRICT'))


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, index=True, primary_key=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='comments')
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), )
    post = relationship('Post', backref='comments')
