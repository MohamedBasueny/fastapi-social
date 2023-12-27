from fastapi.testclient import TestClient
from app import models 
from app.main import app 
from app.schemas import UserOut , UserLogin
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db , Base
import pytest 

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0716103235@localhost/fastapi_test"
SQLALCHEMY_DATABASE_URL_testing = "postgresql://postgres:0716103235@postgres/fastapi_test"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL_testing,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#use this to create tables based on the models .... must import Base from database.py

@pytest.fixture(scope="function")
def session():
    #returns a database session and do the cleaning  
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client (session): #returns a test client that overrides the dev database with a test one 
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) 

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com",
                 "password": "123"}
    res = client.post("/users/create-user", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    print(new_user)
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com",
                 "password": "password123"}
    res = client.post("/users/create-user", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# @pytest.fixture
# def token(test_user):
#     from app.oauth2 import create_access_token
#     return create_access_token({"user_id": test_user['id']})


# @pytest.fixture
# def authorized_client(client, token):
#     client.headers = {
#         **client.headers,
#         "Authorization": f"Bearer {token}"
#     }
#     print(token)
#     print(client)
#     return client

@pytest.fixture
def authorized_client(client,test_user):
    from app.schemas import Token
    res2 = client.post("/auth/login" , 
                      data={"username" : test_user["email"] , 
                            "password" : test_user["password"]})
    assert res2.status_code == 200 
    access_token = Token(**res2.json()).access_token
    headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }
    client.headers=headers
    return client
    

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']}
    
    , {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts