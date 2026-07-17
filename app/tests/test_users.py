import pytest
from jose import jwt
from app import schemas

from app.config import settings

# SQLALCHEMY_DATABASE_URL= f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{"test_database"}'
# SECRET_KEY=settings.secret_key
# ALGORITHM=settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES=int(settings.access_token_expire_minutes)


# engine=create_engine(SQLALCHEMY_DATABASE_URL)


# TestSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)




# def override_get_db():
#     db = TestSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db]=override_get_db
# @pytest.fixture(scope="module")
# def client():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)


    

def test_root(client):
    res=client.get("/")

    assert res.json().get("message")=="welcome to this social media app! Use postman or Bruno to test this app,Bruno-collection is uploaded on Git"
    assert res.status_code==200


def test_createuser(client):
    res = client.post("/users/",json={"email":"hello@gmail.com","password":"mypassword"})
    new_user= schemas.userout(**res.json())
    
    assert new_user.email == "hello@gmail.com"
    assert res.status_code==201

def test_login(client,testusr):
    res = client.post("/login",data={"username":"testmail@gmail.com","password":"pass123"})
    data= res.json()
    payload=jwt.decode(data.get('access_token'),settings.secret_key,algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    print("this id respons:",res.json())

    assert id==testusr['id']
    assert res.json().get("token_type") == "bearer"
    assert res.status_code==200