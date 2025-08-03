
from pathlib import Path
import os
from typing import Tuple, Optional, List, Union, Iterable

from fastapi import FastAPI, Depends, Request, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from db.db import init_db, get_session, is_initialized
from models.product import Product
from models.category import Category, CategoryGet
from models.many_to_many import ProductCategoryLink

from utils.database_utils import assign_n_uneven_categories_by_index, get_fake_categories

# from auth import create_access_token, authenticate_user

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
templates.env.globals['static_url'] = 'http://localhost:8082'

BASE_IMAGE_PATH = Path('/static/images')

SECRET_KEY = os.environ['SECRET_KEY']
ORIGINS = os.environ.get('FRONTEND_URL') or []

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event("startup")
async def on_startup():
    print('bob')
    try:
        x = await is_initialized()
        if x == True:
            return
        await init_db()

        print('initialized database')
        num_images = 50000
        created_categories = get_fake_categories()
        async for session in get_session():
            session.add_all(created_categories)
            for i in range(1, num_images+1):
                product = Product(
                    name=f'product-{i}',
                    description='',
                    file_path= str(Path('/static/images') / Path('products') / f'{i}.jpg')
                )
                categories = assign_n_uneven_categories_by_index(i=i, categories=created_categories, n=3)
                product.categories = categories
                session.add(product)
            await session.commit()
    except Exception as e:
        raise NotImplemented(e)

@app.get('/hello')
def hello():
    print('1')
    return 'worldx'


@app.get('/json')
async def return_json():
    return {'bob': 1}

@app.get('/product')
def test(request: Request):
    
    return templates.TemplateResponse("product.html", {"request": {}})

@app.get('/category/{category_id}')
def test(request: Request):

    return templates.TemplateResponse("products-list.html", {"request": {}})

@app.get('/testusercreate')
async def product_create(request: Request, session=Depends(get_session)):
    product = Product(name='bob')

    return '1'

@app.get('/getimage')
def testimage(request: Request):
    return templates.TemplateResponse('image.html', {'request': request}) 

@app.get('/query')
async def querytest(session = Depends(get_session)):
    stmt = select(Product).where(Product.id == 1)
    result = await session.execute(stmt)
    prod = result.scalars().one()
    return prod

@app.get('/query/many')
async def querytest(session = Depends(get_session)):
    user_ids = [1, 100, 300]
    stmt = select(Product).where(Product.id.in_(user_ids))
    result = await session.execute(stmt)
    prods = result.scalars().all()
    return prods

@app.get('/products')
async def list_products(
    request: Request,
    offset: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=25), 
    session = Depends(get_session)
):
    stmt = select(Product).offset(offset).limit(limit)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return templates.TemplateResponse(
        'products-list.html',
        {'products': products, 'request': request}
    )

@app.get('/categoriesforproduct/{product_id}')
async def get_categories_for_product(product_id: int, session = Depends(get_session)) -> list[CategoryGet]:
    stmt = select(Category) \
        .join(ProductCategoryLink, ProductCategoryLink.category_id == Category.id) \
        .where(ProductCategoryLink.product_id == product_id)
    result = await session.execute(stmt)
    return result.scalars().all()
    