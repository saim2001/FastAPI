from datetime import datetime
from typing import  Optional

from pydantic import BaseModel, EmailStr, conint


class User(BaseModel):
    user_email:EmailStr
    user_password:str

class ResUser(BaseModel):
    user_email:EmailStr
    user_id:int
    user_created_at:datetime
    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    user_email:EmailStr
    user_password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class Token_Data(BaseModel):
    user_id:Optional[str]=None

class PostBase(BaseModel):
    post_title: str
    post_content: str
    post_published: bool = True

class PostCreate(PostBase):
    pass

class ResPost(PostBase):
    post_id:int
    post_created_at:datetime
    owner_id:int
    post_owner:ResUser

    class Config:
        orm_mode=True

class Like(BaseModel):
    like_post_id:int
    like_dir: conint(ge=0,le=1)

class Post_W_Likes(BaseModel):
    POST:ResPost
    likes: int

    class Config:
        orm_mode = True


