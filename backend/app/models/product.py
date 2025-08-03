from decimal import Decimal
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from models.category import Category, CategoryGet
from models.many_to_many import ProductCategoryLink
from pydantic import FilePath

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    brand: str | None = Field(max_length=256)
    price: Decimal | None = Field(gt=0, description='Price of the product')
    description: Optional[str] = Field(default=None, max_length=500)
    stock: Optional[int] = Field(ge=0, default=0)
    file_path: FilePath = Field(default=None, max_length=1000)

    categories: List[Category] = Relationship(back_populates="products", link_model=ProductCategoryLink)


class ProductGet(SQLModel):
    id: int
    name: str
    brand: Optional[str]
    description: Optional[str]
    stock: Optional[int]
    file_path: Optional[str]
    categories: List[Category] = []