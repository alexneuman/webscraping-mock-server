
from typing import Optional

import bcrypt
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidSignatureError
import jwt
import os
from sqlmodel.ext.asyncio.session import AsyncSession


oauth2_scheme = OAuth2PasswordBearer('login')

SECRET_KEY = os.environ['SECRET_KEY']

def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: bytes, password_hash: bytes):
    return bcrypt.checkpw(password, password_hash)

def authenticate_user(password: str, password_hash: str):
    passwords_match = check_password(password.encode(), password_hash.encode())
    if not passwords_match:
        raise ValueError
    
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')