from datetime import datetime, timedelta
from typing import Annotated
from . import crud, schemas, models
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . database import SessionLocal, engine

SECRET_KEY = "86d9d628a7e6a6992b1f39ad9db0c9fb8bc7e7df87afe4a77f8be6de817e5104"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


def authenticate_user(username: str , password: str,db: Session  = Depends(get_db)):
    user = crud.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session  = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session  = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=schemas.User)
# async def read_users_me(
#     current_user: Annotated[models.User, Depends(get_current_active_user)] #TODO check if model is being turned into chema
# ):
#     return current_user

@app.post("/signup")
async def signup(username: str, password: str,db: Session  = Depends(get_db)):
    hashed_password=get_password_hash(password)
    new_user=schemas.User(username=username)
    crud.create_user(db,new_user,hashed_password=hashed_password)
    token_data={"sub": username}
    access_token = create_access_token(token_data)
    return{"access_token": access_token, "token_type":"bearer"}

@app.post("/addtask")
async def add_task(current_user: Annotated[models.User, Depends(get_current_active_user)]
                   ,task: schemas.Task,db :Session= Depends(get_db)):
    task.user=current_user
    crud.create_task(db,task)
    return {"message": "Task added successfully"}
    
    

@app.post("/rmtask")
async def remove_task(current_user: Annotated[models.User, Depends(get_current_active_user)]
                   ,task: schemas.Task,db :Session= Depends(get_db)):
    task.user=current_user
    crud.rm_task(db,task)
    return {"message":"Task deleted successfully"}

@app.post("/updatetask")
async def update_task(current_user: Annotated[models.User, Depends(get_current_active_user)]
                   ,task: schemas.Task,db :Session= Depends(get_db)):
    task.user=current_user
    crud.update_task(db,task)
    return {"message":"Task updated successfully"}
    

@app.post("/changestattask")
async def change_status_task(current_user: Annotated[models.User, Depends(get_current_active_user)]
                   ,task: schemas.Task,db :Session= Depends(get_db)):
    task.user=current_user
    crud.change_task_stat(db,task)
    return {"message" : "Task status changed successfully"}
# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]