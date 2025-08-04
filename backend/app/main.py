
from pathlib import Path
from math import ceil
import os
from typing import Tuple, Optional, List, Union, Iterable

from fastapi import FastAPI, Depends, Request, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from sqlmodel import select
from app.db.db import init_db, get_session, is_initialized
from app.models.product import Product, ProductGet
from app.models.category import Category, CategoryGet
from app.models.many_to_many import ProductCategoryLink

from app.utils.database_utils import assign_n_uneven_categories_by_index, get_fake_categories, generate_fake_price, generate_fake_string
from app.utils.pagination import enforce_max_total
from app.utils.dummy_data import generate_dummy_data

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

# @app.on_event("startup")
async def on_startup():
    await init_db()
    await generate_dummy_data()
  

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


async def get_category(
        category_slug: str | None = Query(None, alias="category"),
        session=Depends(get_session)
):
    if not category_slug:
        return 
    stmt = select(Category).where(Category.slug == category_slug)
    result = await session.execute(stmt)
    category = result.scalars().first()
    return category

async def get_all_categories(
        session = Depends(get_session)
):
    stmt = select(Category)
    results = await session.execute(stmt)
    categories = results.scalars().all()
    return categories

@app.get('/products')
async def list_products(
    request: Request,
    offset: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=25),  # limit must be ≥ 1
    session = Depends(get_session),
    category_name: None|str = Query(None, alias='category'),
    categories = Depends(get_all_categories)
    # category: Category|None = Depends(get_category)
):
    stmt = select(Product).offset(offset).limit(limit)
    if category_name:
        # stmt = stmt.where(Category.slug == category_name)
        stmt = stmt.join(Product.categories).where(Category.slug == category_name)
    pagination_total = 5000
    enforce_max_total(offset, limit, pagination_total)

    # Fetch paginated products
    
    result = await session.execute(stmt)
    products = result.scalars().all()

    total_stmt = select(func.count(Product.id))
    # total_stmt = select(func.count()).select_from(Product)
    if category_name:
        total_stmt = (
        total_stmt
        .join(Product.categories)
        .where(Category.slug == category_name)
    )
    total_db = await session.scalar(total_stmt)
    
    total = min(total_db, pagination_total)
    max_pages = ceil(total / limit) if total > 0 else 1
    current_page = (offset // limit) + 1

    # Compute safe start/end page for pagination
    start_page = max(1, current_page - 2)
    end_page = min(max_pages, current_page + 2)

    return templates.TemplateResponse(
        'pages/products-listings-page.html',
        {
            'request': request,
            'products': products,
            'current_page': current_page,
            'max_pages': max_pages,
            'start_page': start_page,
            'end_page': end_page,
            'limit': limit,
            'categories': categories
        }
    )


@app.get('/categoriesforproduct/{product_id}')
async def get_categories_for_product(product_id: int, session = Depends(get_session)) -> list[CategoryGet]:
    stmt = select(Category) \
        .join(ProductCategoryLink, ProductCategoryLink.category_id == Category.id) \
        .where(ProductCategoryLink.product_id == product_id)
    result = await session.execute(stmt)
    return result.scalars().all()
    

@app.get("/productwithcategories/{product_id}")
async def get_product_with_categories(
    product_id: int,
    session=Depends(get_session),
):
    stmt = (
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.categories))
    )
    result = await session.execute(stmt)
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get('/productswithcategories2')
async def get_product_with_categories_2(
    product_ids: list[int] = Query(...),
    session=Depends(get_session)
) -> list[Product]:
    stmt = select(Product).where(Product.id.in_(product_ids)).options(selectinload(Product.categories))
    results = await session.execute(stmt)
    products = results.unique().scalars().all()
    return products

async def get_product(
        product: str|None,
        session = Depends(get_session)
):
  
    stmt = select(Product).where(Product.slug == product)
    results = await session.execute(stmt)
    products = results.scalars().first()
    return products  

@app.get('/product/{product}')
def product_details_page(
    request: Request,
    product = Depends(get_product)):
    return templates.TemplateResponse(
        'pages/product-details-page.html',
        {'request': request, 'product': product}
    )
