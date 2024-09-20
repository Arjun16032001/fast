from fastapi import FastAPI, Depends, HTTPException,requests
from sqlalchemy.orm import Session
from models import User,Blog  
from schemas import UserCreate, UserResponse, UserBase,UserBlog
from database import engine, get_db
from passlib.context import CryptContext
from typing import List
from utils import create_access_token,create_refresh_token
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta,timezone
import requests
from requests import get
from pydantic import EmailStr
import jwt
import os

app = FastAPI()


User.metadata.create_all(bind=engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)#pass hashing

def verify_password(hashed_password,plain_password):
    return pwd_context.verify(hashed_password,plain_password)#for login

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user #to databse




@app.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
  return create_user(db=db, user=user)

@app.get("/users/",response_model=list[UserResponse])
def get_user(db: Session=Depends(get_db)):
    users=db.query(User).all()
    return users
    


@app.post('/login/')
def login_user(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    users=db.query(User).filter(User.username==user.username).first()
    if not users:
        raise HTTPException(status_code=401,detail="invalid credentials")
    if not verify_password(user.password,users.hashed_password):
        raise HTTPException(status_code=401,detail="invalid credentials")
    access_token= create_access_token(users.username)
    refresh_token= create_refresh_token(users.username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjYwMzc4OTUsInN1YiI6ImFyanVuQGdtYWlsLmNvbSJ9.vuVZjNa20Q0M_qtte3JNcN8yPynXxfJ_5pn24Qs47Wc"
# headers = {"Authorization": f"Bearer {access_token}"}
# response = requests.get("http://127.0.0.1:8000/items/", headers=headers)



JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY','default_secret_key')#token from env
ALGORITHM = "HS256"

def get_current(token:str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    try:
        gathered=jwt.decode(token,JWT_SECRET_KEY,algorithms=[ALGORITHM])
        username:str=gathered.get("sub")
        if not username:
            raise HTTPException(status_code=401,detail="unable to validate")
    except:
        raise HTTPException(status_code=401,detail="unable to validate")
    
    user=db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=401,detail="unable to validate")
    return user

@app.get('/gathers/user_listing')
def read_user(user:User=Depends(get_current)):
    return user

@app.post('/write_blog/',response_model=UserBlog)
def write_blog(user:UserBlog,db:Session=Depends(get_db),auth_user:User=Depends(get_current)):
    db_user=Blog(title=user.title,content=user.content)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get('/read_blogs/',response_model=list[UserBlog])
def read_blog(db:Session=Depends(get_db),auth_user:User=Depends(get_current)):
    db_user=db.query(Blog).all()
    return db_user