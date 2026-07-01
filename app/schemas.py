from datetime import datetime
from typing import Optional


from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PoseCreate(PostBase):
    pass

class userout(BaseModel):
    id: int
    email:EmailStr
    createdat: datetime
    class Config:
        orm_mode=True

class Post(PostBase):
    id: int
    createdat: datetime
    owner_id: int
    owner:userout
    class Config:
        orm_mode=True

class postout(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode=True
 
class usercreate(BaseModel):
    email:EmailStr
    password:str



class userlogin(BaseModel):
    email:EmailStr 
    password:str

class token(BaseModel):
    access_token: str
    token_type:str

class tokendata(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir: int


