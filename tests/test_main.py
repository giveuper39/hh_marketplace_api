import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import db
from app.models import Category, Tag, Item, ItemTag

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    if db.is_closed():
        db.connect()
    db.create_tables([Category, Tag, Item, ItemTag])

    yield

    db.drop_tables([Category, Tag, Item, ItemTag])
    db.close()


def create_category(name="TestCategory"):
    response = client.post("/categories", json={"name": name})
    return response.json()["id"]


def create_tag(name="TestTag"):
    response = client.post("/tags", json={"name": name})
    return response.json()["id"]


def clear():
    Item.delete()
    Tag.delete()
    Category.delete()
    ItemTag.delete()


def create_item(
    name="TestItem",
    description="Test description for test item",
    price="100",
    category_id=None,
    tags=None,
):
    if tags is None:
        tags = []
    item_data = {
        "name": name,
        "description": description,
        "price": price,
        "category_id": category_id,
        "tags": tags,
    }
    response = client.post("/items", json=item_data)
    return response


def test_create_category():
    clear()
    response = client.post("/categories", json={"name": "TestCategory"})
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "TestCategory"
    assert "id" in data


def test_create_tag():
    clear()
    response = client.post("/tags", json={"name": "TestTag"})
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "TestTag"
    assert "id" in data


def test_create_item():
    clear()
    category_id = create_category()
    tag_id1 = create_tag("TestTag1")
    tag_id2 = create_tag("TestTag2")

    response = create_item(category_id=category_id, tags=[tag_id1, tag_id2])
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "TestItem"
    assert data["price"] == 100
    assert data["category"]["id"] == category_id
    assert len(data["tags"]) == 2
    assert data["tags"][0]["id"] == tag_id1


def test_get_item():
    clear()
    category_id = create_category()
    response = create_item(category_id=category_id)
    item_id = response.json()["id"]

    response = client.get(f"/items/{item_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == item_id
    assert data["name"] == "TestItem"


def test_update_item():
    clear()
    category_id = create_category()
    tag = create_tag("TestTag")
    response = create_item(category_id=category_id)
    item_id = response.json()["id"]

    update_data = {
        "name": "TestItemUpdated",
        "description": "Test item description, updated",
        "price": "2000",
        "category_id": category_id,
        "tags": [tag],
    }

    response = client.put(f"/items/{item_id}", json=update_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "TestItemUpdated"
    assert data["description"] == "Test item description, updated"
    assert len(data["tags"]) == 1
    assert data["price"] == 2000


def test_delete_item():
    clear()
    category_id = create_category()
    response = create_item(category_id=category_id)
    item_id = response.json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_filter_items():
    clear()
    category_id = create_category()
    tag_id1 = create_tag("TestTag1")
    tag_id2 = create_tag("TestTag2")

    create_item(name="TestItem1", category_id=category_id, tags=[tag_id1, tag_id2])
    create_item(name="TestItem2", category_id=category_id, tags=[tag_id2])

    response = client.get(f"/items?category_id={category_id}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2

    response = client.get(f"/items?&tag_ids={tag_id2}tag_ids={tag_id2}")
    data = response.json()
    print(data)

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "TestItem1"
