from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, conint
from datetime import datetime


# * This file is used to define SCHEMAS/PYDANTIC MODEL for REQUEST and RESPONSE


#! This CLASS is schema/Pydantic model for fastAPI define structure of a request & response
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


#! Create "user" REQUEST Model definition
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    name: str


#! Create "user" RESPONSE Model definition
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


#! This class is used for create post API which inherits from PostBase class
class CreatePost(PostBase):
    pass


#! This class is used for Update post API which inherits from PostBase class
class UpdatePost(PostBase):
    pass


# * These below classes are for response schema/pydantic model (what user sees as RESPONSE)


#! Create "POST" RESPONSE Model definition
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    # ! we should add this class because API returns a SQL response which is not understood by FastAPI as it only understands dictionaries
    class Config:
        from_attributes = True


# ! This schema is for votes
class PostVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


# ! User authentication schema
class AuthenticateUser(BaseModel):
    email: EmailStr
    password: str


# ! User Token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
