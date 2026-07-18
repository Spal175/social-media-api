#API-Driven Seeding:
def test_getallposts(authorized_client,test_posts):
    res=authorized_client.get("/posts")
    print("this is my get all response",res.json())
    assert res.status_code==200
#Database/ORM Seeding: 
def  test_getallposts2(authorized_client,testposts2):
    res=authorized_client.get("/posts")
    print("this is my get all response",res.json())
    assert res.status_code==200

