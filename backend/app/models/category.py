from typing import Optional, List
from slugify import slugify

from sqlalchemy import event
from sqlmodel import SQLModel, Field, Relationship
from pydantic import FilePath, field_validator
from app.models.many_to_many import ProductCategoryLink

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    slug: str = Field(max_length=128)

    products: List["Product"] = Relationship(back_populates="categories", link_model=ProductCategoryLink)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.name.lower()
        self.slug = self.slug or slugify(self.name)

    # @event.listens
    # def generate_slug(cls, v, values):
    #     if v:
    #         return v
    #     name = v.get('name')
    #     return slugify(name)


class CategoryGet(SQLModel):
    name: str = Field(index=True, max_length=100)