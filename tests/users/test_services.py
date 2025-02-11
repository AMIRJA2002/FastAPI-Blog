# from core.users.services import create_user, login_user
# from core.users.schemas import UserCreate, UserLogin
# from core.users.models import User, Role
# from fastapi import HTTPException
# from tests.test_database import *
#
#
# def test_create_user(db_session):
#     user_data = UserCreate(
#         username='amir',
#         email='amir@amasasasir.com',
#         password='amir',
#         role='admin'
#     )
#
#     data = create_user(user_data, db_session)
#     user = db_session.query(User).filter(User.username == user_data.username).first()
#
#     assert user.role == Role.admin
#     assert user.username == user_data.username
#     assert data == {'data': 'user has been created'}
#
#
# def test_create_user_with_username(db_session):
#     user = User(username='amir1', email='test@test.com', role='admin')
#     db_session.add(user)
#     db_session.commit()
#
#     user_data = UserCreate(
#         username='amir1',
#         email='amir@amasasasir.com',
#         password='amir',
#         role='admin'
#     )
#
#     with pytest.raises(HTTPException) as exc_info:
#         create_user(user_data, db_session)
#
#     assert exc_info.value.status_code == 400
#     assert exc_info.value.detail == "username of email already exists"
#
#
# def test_login(db_session):
#     user = User(username='amir1', email='test@test.com', role='admin')
#     user.hash_password('amir')
#
#     db_session.add(user)
#     db_session.commit()
#
#     user_data = UserLogin(
#         username='amir1',
#         password='amir',
#     )
#
#     data = login_user(user_data, db_session)
#     response = data.model_dump()
#
#     assert 'access_token' in response
#     assert 'token_type' in response
#
#
# def test_login_failed(db_session):
#     user_data = UserLogin(
#         username='amir1',
#         password='amir',
#     )
#
#     with pytest.raises(HTTPException) as exc_info:
#         login_user(user_data, db_session)
#
#     assert exc_info.value.status_code == 401
#     assert exc_info.value.detail == "invalid username or password"
