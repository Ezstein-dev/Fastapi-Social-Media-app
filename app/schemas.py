from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from typing import List


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner: User

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True


class Comment(BaseModel):
    user_id: int
    comment: str
    created_at: datetime

    class Config:
        orm_mode = True

class CommentOut(BaseModel):
    Comment: Comment
    likes: int

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    comment: str
    published: bool= True

class PostCommentOut(BaseModel):
    post: List[PostOut]
    comments: List[CommentOut]
    
    class Config:
        orm_mode = True

class PostVote(BaseModel):
    post_id: int
    dir: conint(le=1)


class CommentVote(BaseModel):
    comment_id: int
    dir: conint(le=1)
