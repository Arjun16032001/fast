import os
from datetime import datetime, timedelta,timezone
from typing import Union, Any
import jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException
from database import get_db
from pydantic import EmailStr
from models import User  



ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=60
ALGORITHM = "HS256"
JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY','default_secret_key')#token from env
JWT_REFRESH_SECRET_KEY=os.getenv('JWT_REFRESH_SECRET_KEY','default_secret_key')
#token creation
def create_access_token(subject:str,expires_delta: timedelta = None):
    if expires_delta :
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str,expires_delta: timedelta = None) :
    if expires_delta :
        expires_delta =datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
#token decoding for userlisting




    

