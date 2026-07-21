#API-Driven Seeding:
from app import schemas
import pytest

def test_getallposts(authorized_client,test_posts):
    res=authorized_client.get("/posts")
    print("this is my get all posts response",res.json())

    assert len(res.json())==len(test_posts)
    assert res.status_code==200
#Database/ORM Seeding: 
def  test_getallposts2(authorized_client,testposts2):
    res=authorized_client.get("/posts")
    print("this is my get all response",res.json())
    assert res.status_code==200

def test_unauthorized_user_get_all_posts(client, testposts2):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, testposts2):
    res = client.get(f"/posts/{testposts2[0].id}")
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


def test_get_one_post_not_exist(authorized_client, testposts2):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])

def test_create_posts(authorized_client,testposts2,title,content,published,testusr):
    res=authorized_client.post('/posts/createposts',json={"title":title,"content":content,"published":published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == testusr['id']

def test_unauthorized_user_create_post(client, testusr, testposts2):
    res = client.post(
        "/posts/createposts", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401

def test_update_post(authorized_client, testusr, testposts2):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": testposts2[0].id

    }
    res = authorized_client.put(f"/posts/{testposts2[0].id}", json=data)
    print(res.status_code)
    print("HAHA",res.json())
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_delete_post_success(authorized_client, testusr, testposts2):
    res = authorized_client.delete(
        f"/posts/{testposts2[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, testusr, testposts2):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


