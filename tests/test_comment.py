from app.schemas import *
import pytest
from jose import jwt
from app.config import settings


@pytest.mark.parametrize("comment, published, status_code",[
    ("This is a comment content", True, 201),
    ("This is a comment content", False, 201)
])
def test_create_comment(authorized_client, test_posts, test_user, comment, published, status_code):
    comment_data = {"comment": comment, "published": published}
    res = authorized_client.post(f"/comments/{test_posts[0].id}", json=comment_data)
    created_comment = Comment(**res.json())
    assert created_comment.user_id == test_user["id"]
    assert created_comment.comment == comment    
    assert res.status_code == status_code
    

def test_invalid_comment(authorized_client, test_posts, test_user):
    comment_data = {"comment": None, "published": True}
    res = authorized_client.post(f"/comments/{test_posts[0].id}", json=comment_data)  
    assert res.status_code == 422
    
def test_unauthorized_user_create_comment(client, test_posts, test_user):
    comment_data = {"comment": "This is a comment content", "published": True}
    res = client.post(f"/comments/{test_posts[0].id}", json=comment_data)
    assert res.status_code == 401
    
def test_default_create_comment_published_true(authorized_client, test_posts, test_user):
    comment_data = {"comment": "This is a comment content"}
    res = authorized_client.post(f"/comments/{test_posts[0].id}", json=comment_data)
    assert res.status_code == 201
    
def test_get_all_post_comment(authorized_client, test_posts, test_user, test_comments):
    res = authorized_client.get(f"/comments/post/{test_posts[0].id}")
    
    post_comments_list  = res.json()["comments"]
    assert res.status_code == 200
    assert post_comments_list[0]["Comment"]["user_id"] == test_comments[0].user_id
    
def test_unauthoriz_get_all_post_comment(client, test_posts, test_user, test_comments):
    res = client.get(f"/comments/post/{test_posts[0].id}")    
    assert res.status_code == 401

def test_post_comment_post_not_exist(authorized_client, test_posts, test_user, test_comments):
    res = authorized_client.get("/comments/post/700")    
    assert res.status_code == 404
    
def test_get_one_post_comment(authorized_client, test_posts, test_user, test_comments):
    res = authorized_client.get(f"/comments/{test_comments[3].id}")
    comment = CommentOut(**res.json())
    assert comment.Comment.user_id == test_user["id"]
    assert comment.Comment.comment == test_comments[3].comment
    assert res.status_code == 200
    
def test_unauthorize_get_one_post_comment(client, test_posts, test_user, test_comments):
    res = client.get(f"/comments/{test_comments[3].id}")    
    assert res.status_code == 401

def test_get_one_post_comment_not_exist(authorized_client, test_posts, test_user, test_comments):
    res = authorized_client.get("/comments/700")    
    assert res.status_code == 404

def test_delete_post_comment_success(authorized_client, test_user, test_posts, test_comments):
    res = authorized_client.delete(f"/comments/{test_comments[2].id}")    
    assert res.status_code == 204

def test_unauthorize_delete_post_comment(client, test_posts, test_user, test_comments):
    res = client.delete(f"/comments/{test_comments[3].id}")    
    assert res.status_code == 401

def test_delete_other_user_post_comment(authorized_client, test_posts, test_user, test_comments):
    res = authorized_client.delete(f"/comments/{test_comments[0].id}")    
    assert res.status_code == 403

def test_delete_post_comment_not_exist(authorized_client, test_user, test_posts, test_comments):
    res = authorized_client.delete("/comments/700")    
    assert res.status_code == 404

def test_update_post_comment_success(authorized_client, test_user, test_posts, test_comments):
    comment_data = {
        "comment": "This is an updated comment"
    }
    res = authorized_client.put(f"/comments/{test_comments[2].id}", json=comment_data)
    updated_comment = Comment(**res.json())
    assert updated_comment.user_id == test_user["id"]
    assert updated_comment.comment == test_comments[2].comment
    assert res.status_code == 200

def test_unauthorize_update_post_comment(client, test_posts, test_user, test_comments):
    comment_data = {
        "comment": "This is an updated comment"
    }
    res = client.put(f"/comments/{test_comments[2].id}", json=comment_data)    
    assert res.status_code == 401

def test_update_other_user_post_comment(authorized_client, test_posts, test_user, test_comments):
    comment_data = {
        "comment": "This is an updated comment"
    }
    res = authorized_client.put(f"/comments/{test_comments[0].id}", json=comment_data)    
    assert res.status_code == 403
    
def test_update_post_comment_not_exist(authorized_client, test_user, test_posts, test_comments):
    comment_data = {
        "comment": "This is an updated comment"
    }
    res = authorized_client.put("/comments/700", json=comment_data)     
    assert res.status_code == 404