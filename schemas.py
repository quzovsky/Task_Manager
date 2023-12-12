from pydantic import BaseModel
from enum import Enum


class StatusEnum(Enum):
    done='Done.'
    in_progress= 'In progress.'
    completed= 'Completed.'


class User(BaseModel):
    username: str
    disabled: bool | None = None



class Task(BaseModel):
    title : str
    status : StatusEnum
    user : User 



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



class UserInDB(User):
    hashed_password: str

