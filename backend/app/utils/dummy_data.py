from pathlib import Path

from app.models.category import Category
from app.models.product import Product

from app.utils.database_utils import get_fake_categories, generate_fake_price, generate_fake_string, assign_n_uneven_categories_by_index
from app.db.db import get_session
from sqlalchemy.future import select


async def generate_dummy_data():
    print('inserting dummy data')
    num_images = 50000
    created_categories = get_fake_categories()
    async for session in get_session():
        result = await session.execute(select(Product).limit(1))
        existing = result.scalar_one_or_none()
        if existing:
            print('dummy data already exists — skipping insertion')
            return
        session.add_all(created_categories)
        for i in range(1, num_images+1):
            product = Product(
                description='',
                file_path= str(Path('/static/images') / Path('products') / f'{i}.jpg')
            )
            suffix = generate_fake_string(i, num_images)
            price = generate_fake_price(i, num_images, max_price=20000)
            categories = assign_n_uneven_categories_by_index(i=i, categories=created_categories, n=3)
            product.categories = categories
            product.price = price
            product.name=f'product {i} {suffix}'
            product.slug = product.name.replace(' ', '-')
            session.add(product)
        await session.commit()