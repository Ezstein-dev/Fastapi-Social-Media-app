from app.schemas import *
import pytest
from jose import jwt
from app.config import settings


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[3].Post.id == test_posts[0].id


def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorised_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_posts_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/500")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert res.status_code == 200


def test_get_my_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/my_posts")

    def validate(post):
        return PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert posts_list[0].Post.id == test_posts[0].id
    assert posts_list[0].Post.content == test_posts[0].content
    assert posts_list[0].Post.title == test_posts[0].title
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published , status_code", [
    ("valid post", "This is the valid content", True, 201),
    ("valid post", "This is the valid content", False, 201),
])
def test_create_post(authorized_client, test_posts, test_user, title, content, published, status_code):
    post_data = {"title": title, "content": content, "published": published}
    res = authorized_client.post("/posts", json=post_data)
    created_post = Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_user["id"]
    assert res.status_code == status_code


@pytest.mark.parametrize("title, content, published, status_code", [
    (None, "This is the valid content", True, 422),
    ("valid post", None, True, 422),
])
def test_invalid_post(authorized_client, test_posts, test_user, title, content, published, status_code):
    post_data = {"title": title, "content": content, "published": published}
    res = authorized_client.post("/posts", json=post_data)
    assert res.status_code == status_code
    
def test_create_post_default_published_true(authorized_client, test_posts, test_user):
    post_data = {"title": "Post title", "content": "This is the post content"}
    res = authorized_client.post("/posts", json=post_data)
    created_post = Post(**res.json())
    assert created_post.title == "Post title"
    assert created_post.content == "This is the post content"
    assert created_post.published == True
    assert created_post.owner.id == test_user["id"]
    assert res.status_code == 201


def test_unauthorised_user_create_post(client, test_user, test_posts):
    post_data = {"title": "Post title", "content": "This is the post content"}
    res = client.post("/posts", json=post_data)
    assert res.status_code == 401
    
def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/700")
    assert res.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "This is the updated content"
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = Post(**res.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.published == True
    assert updated_post.owner.id == test_user["id"]
    assert res.status_code == 200
    
def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "This is the updated content"
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403
    
def test_unauthorised_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "This is the updated content"
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401
    
def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "This is the updated content"
    }
    res = authorized_client.put(f"/posts/700", json=data)
    assert res.status_code == 404