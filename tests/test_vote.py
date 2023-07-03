from app.schemas import *
import pytest
from jose import jwt
from app.config import settings

def test_vote_on_post(authorized_client, test_posts, test_user):
    data = {
        "post_id": f"{test_posts[3].id}",
        "dir": 1
    }
    res = authorized_client.post("/vote/post/", json=data)
    assert res.status_code == 201
    
def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    data = {
        "post_id": f"{test_posts[0].id}",
        "dir": 1
    }
    res = authorized_client.post("/vote/post/", json=data)
    assert res.status_code == 409
    
def test_delete_vote(authorized_client, test_posts, test_vote):
    data = {
        "post_id": f"{test_posts[0].id}",
        "dir": 0
    }
    res = authorized_client.post("/vote/post/", json=data)
    assert res.status_code == 201
    

def test_delete_vote_non_exist(authorized_client, test_posts):
    data = {
        "post_id": f"{test_posts[0].id}",
        "dir": 0
    }
    res = authorized_client.post("/vote/post/", json=data)
    assert res.status_code == 404
    
def test_vote_post_non_exist(authorized_client, test_posts):
    data = {
        "post_id": 700,
        "dir": 0
    }
    res = authorized_client.post("/vote/post/", json=data)
    assert res.status_code == 404
    
def test_vote_unauthorized_user(client, test_posts):
    data = {
        "post_id": f"{test_posts[0].id}",
        "dir": 0
    }
    res = client.post("/vote/post/", json=data)
    assert res.status_code == 401