def test_getallposts(authorized_client):
    res=authorized_client.get("/posts")
    print("this is my get all response",res.json())
    assert res.status_code==200