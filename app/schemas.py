from pydantic import BaseModel , Field , EmailStr  ,conint
from datetime import datetime 
from typing import Optional

class UserCreate (BaseModel):
    email:EmailStr
    password : str 

class UserOut (BaseModel) :
    id : int 
    created_at : datetime
    email : EmailStr 


class UserLogin (BaseModel) : 
    email : EmailStr 
    password : str 

class Token (BaseModel) : 
    access_token : str 
    token_type : str 

class TokenData (BaseModel):
    id : Optional[str] = None 


#pydantic clases for client side 
class PostBase(BaseModel) :
    title : str =Field(min_length=3)
    content : str = Field(min_length=3)
    published : bool = True 

class PostCreate (PostBase):
    pass 

class PostUpdate (PostBase):
    pass 
#pydantic clases for server side 

class Post (PostBase):
    id:int
    created_at : datetime
    owner_id : int 
    owner : UserOut

    # class config :   #not needed for pydantic2
    #     orm_mode = True 

class PostOut (BaseModel) :
    Post : Post 
    votes : int 
    
class VoteSchema (BaseModel) : 
    post_id : int 
    direction : conint(le=1)

