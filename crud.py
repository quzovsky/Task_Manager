from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas



def get_user(db: Session, username: str):
    user=db.query(models.User).filter(models.User.username==username).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


def create_user(db: Session,user: schemas.User,hashed_password):
    existing_data=db.query(models.User).filter(models.User.username==user.username).first()
    if existing_data:
        raise HTTPException(status_code=403,detail="User already exists")
    db_data=models.User(username=user.username,
                        hashed_password=hashed_password)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

def create_task(db:Session, task: schemas.Task,user):
    existing_task=db.query(models.Task).filter(models.Task.code==task.code).first()
    if existing_task:
        raise HTTPException(status_code=403,detail="Task already exists")
    db_task=models.Task(title=task.title, status=task.status,code=task.code,user=user.username)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

def update_task(db:Session, task: schemas.Task,user):
    existing_task=db.query(models.Task).filter(models.Task.code==task.code).first()
    if existing_task:
        if existing_task.owner==user:
            for key,value in task.__dict__.items():
                setattr(existing_task,key,value)
            db.commit()
            db.refresh(existing_task)
            db.close()
        else:
            raise HTTPException(status_code=403,detail="Permission denied")
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    

def change_task_stat(db: Session, task: schemas.Task, new_stat : str,user):
    existing_task=db.query(models.Task).filter(models.Task.code==task.code).first()
    if existing_task:
        if existing_task.owner==user:
            existing_task.status=new_stat
            db.commit()
            db.refresh(existing_task)
            db.close()
        else:
            raise HTTPException(status_code=403,detail="Permission denied")
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    
def rm_task(db: Session, task: schemas.Task,user):
    existing_task=db.query(models.Task).filter(models.Task.code==task.code).first()
    if existing_task:
        if existing_task.owner==user:
            db.delete(existing_task)
            db.commit()
            db.close()
        else:
            raise HTTPException(status_code=403,detail="Permission denied")
    else:
        raise HTTPException(status_code=404, detail="Task not found")