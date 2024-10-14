from pydantic import BaseModel
from typing import List, Optional


class CategorySchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class TagSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ItemBaseSchema(BaseModel):
    name: str
    description: Optional[str]
    price: int
    category_id: int

    class Config:
        from_attributes = True


class ItemCreateSchema(ItemBaseSchema):
    tags: Optional[List[int]] = []


class ItemUpdateSchema(ItemBaseSchema):
    tags: Optional[List[int]] = []


class ItemResponseSchema(ItemBaseSchema):
    id: int
    category: CategorySchema
    tags: List[TagSchema]
    price: int

    class Config:
        from_attributes = True
