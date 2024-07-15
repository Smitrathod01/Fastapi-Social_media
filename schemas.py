from pydantic import BaseModel,EmailStr,conint
from typing import Optional
from datetime import datetime


#regarding users
class Userss(BaseModel):
    email:EmailStr
    username:str
    password:str

class showUser(BaseModel):
    email:EmailStr
    username:str
    

#regarding posts
class Post(BaseModel):
    title:str
    content:str
    published:Optional[bool]


class showPost(BaseModel):
    title:str
    content:str
    published:bool
    created_at: datetime
    creater_id:int
    creator:showUser 

class showlikepost(BaseModel):
    title:str
    content:str
    created_at:datetime


#regarding authentication
class authentication(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


#regarding likes
class likes(BaseModel):
    post_id : int
    like_dir :int

class showlikes(BaseModel):
    post_id : int
    user_id :int

    post:showlikepost
    user:showUser
    


