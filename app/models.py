from peewee import Model, CharField, TextField, IntegerField, ManyToManyField, ForeignKeyField
from .db import db


class Tag(Model):
    name = CharField(max_length=255, unique=True)

    class Meta:
        database = db


class Category(Model):
    name = CharField(max_length=255, unique=True)

    class Meta:
        database = db


class Item(Model):
    name = CharField(max_length=255, unique=True)
    description = TextField(null=True)
    category = ForeignKeyField(Category, backref="items")
    price = IntegerField()
    tags = ManyToManyField(Tag, backref="items")

    class Meta:
        database = db


ItemTag = Item.tags.get_through_model()
