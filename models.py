from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__='Users'
    username = Column(String,primary_key=True,index=True,unique=True)
    hashed_password= Column(String,unique=True)
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__='Tasks'
    title = Column(String)
    status= Column(String)
    code=Column(String,unique=True,primary_key=True)
    user=Column(String,ForeignKey("Users.username"))
    owner = relationship("User", back_populates="tasks")
