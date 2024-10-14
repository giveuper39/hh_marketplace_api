from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .models import Item, Category, Tag, ItemTag
from .schemas import ItemCreateSchema, ItemUpdateSchema, ItemResponseSchema, CategorySchema, TagSchema
from .db import db
from typing import Optional, List


@asynccontextmanager
async def lifespan(app: FastAPI):
    if db.is_closed():
        db.connect()
    db.create_tables([Item, Category, Tag, ItemTag])

    yield

    if not db.is_closed():
        db.close()


app = FastAPI(lifespan=lifespan)


@app.post("/categories")
def create_category(category: CategorySchema) -> CategorySchema:
    category = Category.create(name=category.name)
    return category


@app.post("/tags")
def create_tag(tag: TagSchema) -> TagSchema:
    tag = Tag.create(name=tag.name)
    return tag


@app.post("/items", response_model=ItemResponseSchema)
def create_item(item_data: ItemCreateSchema) -> ItemResponseSchema:
    try:
        category = Category.get_by_id(item_data.category_id)
    except Category.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")

    item = Item.create(
        name=item_data.name, description=item_data.description, price=item_data.price, category=category
    )

    if item_data.tags:
        tags = Tag.select().where(Tag.id.in_(item_data.tags))
        item.tags.add(tags)
    print(item.id, item.name, item.description, item.price)
    return item


@app.get("/items", response_model=List[ItemResponseSchema])
def get_items(category_id: Optional[int] = None, tag_ids: Optional[List[int]] = None) -> List[ItemResponseSchema]:
    query = Item.select()
    if category_id is not None:
        query = query.where(Item.category == category_id)

    if tag_ids is not None:
        query = query.join(ItemTag).where(ItemTag.tag.in_(tag_ids))

    items = list(query)
    print(items)
    return items


@app.get("/items/{item_id}", response_model=ItemResponseSchema)
def get_item(item_id: int) -> ItemResponseSchema:
    try:
        item = Item.get_by_id(item_id)
        return item
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}", response_model=ItemResponseSchema)
def update_item(item_id: int, item_data: ItemUpdateSchema) -> ItemResponseSchema:
    try:
        item = Item.get_by_id(item_id)
        category = Category.get_by_id(item_data.category_id)
        item.name = item_data.name
        item.description = item_data.description
        item.price = item_data.price
        item.category = category
        item.save()

        item.tags.clear()
        if item_data.tags:
            tags = Tag.select().where(Tag.id.in_(item_data.tags))
            item.tags.add(tags)

        return item
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")
    except Category.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        item = Item.get_by_id(item_id)
        item.delete_instance(recursive=True)
        return {"detail": "Item successfully deleted"}
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")
