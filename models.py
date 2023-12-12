from sqlalchemy import Column, Integer, String, JSON, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class User(Base):
    __tablename__='Users'
    username = Column(String,primary_key=True,index=True,unique=True)
    disabled= Column(Boolean,nullable=True) 
    hashed_password= Column(String,unique=True)

class Task(Base):
    __tablename__='Tasks'
    #id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String)
    status= Column(String)
    code=Column(String,unique=True,primary_key=True)

# class Token(Base):
#     access_token = Column(String,unique=True)



# class UserInDB(User):
#     hashed_password: str

