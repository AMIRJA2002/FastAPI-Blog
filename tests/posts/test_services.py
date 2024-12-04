from core.post.models import Post, Comment
from core.post.schemas import AddComment, CreateUpdatePost
from fastapi import HTTPException

from core.users.models import User
from tests.test_database import *
from faker import Faker
from core.post.services import (
    edit_post_service,
    delete_post_service,
    add_comment_service,
    comments_list_service, create_post_service
)

fake = Faker()


@pytest.fixture()
def test_user_admin(db_session):
    user = User(username=fake.user_name(), password="password", role="admin")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture()
def test_user_author(db_session):
    user = User(username=fake.user_name(), password="password", role="author")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture()
def test_user(db_session):
    user = User(username=fake.user_name(), password="password", role="user")
    db_session.add(user)
    db_session.commit()
    return user


def test_create_post_service_with_admin(db_session, test_user_admin):
    post_data = CreateUpdatePost(title="Test Post", content="Test content", tags=[])
    response = create_post_service(post_data, test_user_admin, db_session)
    assert response.title == "Test Post"
    assert response.content == "Test content"


def test_create_post_service_with_author(db_session, test_user_author):
    post_data = CreateUpdatePost(title="Test Post", content="Test content", tags=[])
    response = create_post_service(post_data, test_user_author, db_session)
    assert response.title == "Test Post"
    assert response.content == "Test content"


def test_create_post_with_user(db_session, test_user):
    post_data = CreateUpdatePost(title="Test Post", content="Test content", tags=[])
    with pytest.raises(HTTPException) as exc_info:
        create_post_service(post_data, test_user, db_session)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "you do not have permission for this action"


def test_edit_post_service_whit_admin(db_session, test_user_admin):
    post = Post(title="Old Title", content="Old Content", author_id=test_user_admin.id)
    db_session.add(post)
    db_session.commit()

    post_data = CreateUpdatePost(title="New Title", content="New Content", tags=[])
    response = edit_post_service(post_data, db_session, post)

    assert response.title == "New Title"
    assert response.content == "New Content"


def test_edit_post_service_author_owner(db_session, test_user_admin, test_user):
    post = Post(title="Old Title", content="Old Content", author_id=test_user.id)
    db_session.add(post)
    db_session.commit()

    post_data = CreateUpdatePost(title="New Title", content="New Content", tags=[])
    response = edit_post_service(post_data, db_session, post)

    assert response.title == "New Title"
    assert response.content == "New Content"


def test_delete_post_service(db_session, test_user_admin):
    post = Post(title="Post to delete", content="Delete this post", author_id=test_user_admin.id)
    db_session.add(post)
    db_session.commit()

    response = delete_post_service(db_session, post)
    assert response["data"] == "post deleted!"
    assert db_session.query(Post).filter(Post.id == post.id).first() is None


def test_add_comment_service(db_session, test_user_admin):
    post = Post(title="Post for comment", content="This post will get a comment", author_id=test_user_admin.id)
    db_session.add(post)
    db_session.commit()

    comment_data = AddComment(content="This is a comment", post_id=post.id)
    response = add_comment_service(comment_data, db_session, test_user_admin)
    assert response.content == "This is a comment"
    assert db_session.query(Comment).filter(Comment.content == "This is a comment").first() is not None


def test_comments_list_service_with_admin(db_session, test_user_admin):
    post = Post(title="Post with comments", content="This post has comments", author_id=test_user_admin.id)
    db_session.add(post)
    db_session.commit()

    comment = Comment(content="First comment", user_id=test_user_admin.id, post_id=post.id)
    db_session.add(comment)
    db_session.commit()

    comment = Comment(content="Second comment", user_id=test_user_admin.id, post_id=post.id)
    db_session.add(comment)
    db_session.commit()

    response = comments_list_service(post.id, db_session, test_user_admin)
    assert len(response.__dict__["comments"]) == 2
    assert response.__dict__["comments"][0].content == "First comment"


def test_comments_list_service_author(db_session, test_user_admin, test_user):
    post = Post(title="Post with comments", content="This post has comments", author_id=test_user.id)
    db_session.add(post)
    db_session.commit()

    comment1 = Comment(content="First comment", user_id=test_user.id, post_id=post.id)
    comment2 = Comment(content="Second comment", user_id=test_user.id, post_id=post.id)
    db_session.add(comment1)
    db_session.add(comment2)
    db_session.commit()

    response = comments_list_service(post.id, db_session, test_user)

    assert len(response.__dict__["comments"]) == 2
    assert response.__dict__["comments"][0].content == "First comment"
    assert response.__dict__["comments"][1].content == "Second comment"


def test_comments_list_service_with_user(db_session, test_user_admin, test_user):
    post = Post(title="Post with comments", content="This post has comments", author_id=test_user_admin.id)
    db_session.add(post)
    db_session.commit()

    comment1 = Comment(content="First comment", user_id=test_user_admin.id, post_id=post.id)
    comment2 = Comment(content="Second comment", user_id=test_user_admin.id, post_id=post.id)
    db_session.add(comment1)
    db_session.add(comment2)
    db_session.commit()

    with pytest.raises(HTTPException) as exc_info:
        comments_list_service(post.id, db_session, test_user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You do not have permission for this action"


def test_comments_list_service_post_not_found(db_session, test_user_admin):
    non_existent_post_id = 'nonexistent_id'

    with pytest.raises(HTTPException) as exc_info:
        comments_list_service(non_existent_post_id, db_session, test_user_admin)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "post not found"
