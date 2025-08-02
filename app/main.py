
import os
from typing import Tuple, Optional, List, Union, Iterable

from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth import create_access_token, authenticate_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

SECRET_KEY = os.environ['SECRET_KEY']
ORIGINS = os.environ.get('FRONTEND_URL') or []

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/hello')
def hello():
    return 'world'

@app.get('/test')
def test(request: Request):
    return templates.TemplateResponse("product.html", {"request": {}}, request=request)


    