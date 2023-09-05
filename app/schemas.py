from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# schemas dictate which data is necessary for the user to provide and the data the server will return to the user
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostRequest(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime
    user: UserResponse

    # make it able to return in a list
    class Config:
        from_attributes = True


class PostVoteResponse(BaseModel):
    # Post is the name of the model returned from the query
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserRequest(UserBase):
    pass


class UserLogin(UserBase):
    pass


class TokenRequest(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    id: Optional[int] = None


class VoteRequest(BaseModel):
    post_id: int
    up_vote: bool
