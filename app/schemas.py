from pydantic import BaseModel
from typing import List, Optional


class CategorySchema(BaseModel):
    name: str


class TagSchema(BaseModel):
    name: str


class ItemBaseSchema(BaseModel):
    name: str
    description: Optional[str]
    price: str
    category_id: int


class ItemCreateSchema(ItemBaseSchema):
    tags: Optional[List[int]] = []


class ItemUpdateSchema(ItemBaseSchema):
    tags: Optional[List[int]] = []


class ItemResponseSchema(ItemBaseSchema):
    id: int
    category: CategorySchema
    tags: List[TagSchema]

    class Config:
        orm_mode = True
