from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import test
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import crtacstkn
from app import models
from alembic import command

from ..schemas import userout


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/test_database'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def testusr(client):
    res=client.post("/users/",json={"email":"testmail@gmail.com","password":"pass123"})
    new_user= userout(**res.json())
    s=res.json()
    print('\n',"this is return of test usr",s)
    yield s

@pytest.fixture
def token(testusr):
    return crtacstkn({"user_id": testusr["id"]})

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"bearer {token}"
    }

    yield client
    client.headers.pop("Authorization", None)

@pytest.fixture
def test_posts(testusr, authorized_client):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": testusr['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": testusr['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": testusr['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": testusr['id']
    }]

    created_posts = []
    for post in posts_data:
        response = authorized_client.post("/posts/createposts", json=post)
        created_posts.append(response.json())

    return created_posts



@pytest.fixture
def testposts2(testusr, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": testusr['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": testusr['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": testusr['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": testusr['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    
    session.commit()

    posts = session.query(models.Post).all()
    return posts    

@pytest.fixture()
def test_vote(testposts2, session, testusr):
    new_vote = models.Votes(post_id=testposts2[3].id, user_id=testusr['id'])
    session.add(new_vote)
    session.commit()

