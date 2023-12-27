def test_vote_on_post(authorized_client, test_posts ):
    data = {
        "post_id" : test_posts[0].id,
        "direction" : 1
    }
    res = authorized_client.post("/vote", json=data)
    assert res.status_code == 201

def test_vote_on_post_by_unautherized_user(client, test_posts ):
    data = {
        "post_id" : test_posts[0].id,
        "direction" : 1
    }
    res = client.post("/vote", json=data)
    assert res.status_code == 401


def test_vote_on_post_not_owned_by_user(authorized_client, test_posts ):#this is ok for now
    data = {
        "post_id" : test_posts[3].id,
        "direction" : 1
    }
    res = authorized_client.post("/vote", json=data)
    assert res.status_code == 201


def test_vote_on_post_not_found(authorized_client, test_posts ):#this is ok for now
    data = {
        "post_id" : 4444,
        "direction" : 1
    }
    res = authorized_client.post("/vote", json=data)
    assert res.status_code == 404



import pytest
from app import models 

@pytest.fixture 
def test_give_post_vote(session , test_user, test_posts) :
    new_vote = models.Vote(post_id = test_posts[3].id , user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post_twice(authorized_client, test_posts, test_give_post_vote ):#this is ok for nowtest_give_post_vote
    data = {
        "post_id" : test_posts[3].id,
        "direction" : 1
    }   
    res = authorized_client.post("/vote", json=data)
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_give_post_vote ):
    data = {
        "post_id" : test_posts[3].id,
        "direction" : 0
    }   
    res = authorized_client.post("/vote", json=data)
    assert res.status_code == 201

def test_delete_vote_not_exist(authorized_client , test_posts) :
    data = {
        "post_id": 333,
        "direction": 0
    }
    res = authorized_client.post("/vote", json=data)
    assert res.status_code == 404