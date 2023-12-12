from pydantic import BaseModel
from enum import Enum


class StatusEnum(str,Enum):
    done='Done.'
    in_progress= 'In progress.'
    completed= 'Completed.'


class User(BaseModel):
    username: str



class Task(BaseModel):
    title : str
    status : StatusEnum
    code : str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



class UserInDB(User):
    hashed_password: str

