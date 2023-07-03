from app.schemas import *
import pytest
from jose import jwt
from app.config import settings
    
    
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Welcome to my api"
#     assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json={"email": "ezsdev@gmail.com", "password": "password234", "phone_number": "4638373837"})
    new_user = UserOut(**res.json())
    assert new_user.email == "ezsdev@gmail.com"
    assert res.status_code == 201
    
def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongmail@gmail.com", "password234", 403),
    ("ezsdev@gmail.com", "wrongPassword", 403),
    ("wrongmail@gmail.com", "wrongPassword", 403),
    (None, "password234", 422),
    ("ezsdev@gmail.com", None, 422)
])
def test_invalid_credentials(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"