def test_vote_on_post(authorized_client, testposts2):
    res = authorized_client.post(
        "/vote/", json={"post_id": testposts2[3].id, "dir": 1})
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, testposts2, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": testposts2[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, testposts2, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": testposts2[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, testposts2):
    res = authorized_client.post(
        "/vote/", json={"post_id": testposts2[3].id, "dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, testposts2):
    res = authorized_client.post(
        "/vote/", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, testposts2):
    res = client.post(
        "/vote/", json={"post_id": testposts2[3].id, "dir": 1})
    assert res.status_code == 401