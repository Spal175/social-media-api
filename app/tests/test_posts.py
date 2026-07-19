#API-Driven Seeding:
from app import schemas


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
    post=schemas.postout(**res.json())
    assert res.status_code == 401
    assert post.Post.id==testposts2[0].id
    assert post.Post.content==testposts2[0].content
    assert post.Post.title==testposts2[0].title


def test_get_one_post_not_exist(authorized_client, testposts2):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404