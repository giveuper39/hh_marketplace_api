from peewee import SqliteDatabase
from .config import settings


# db = PostgresqlDatabase(
#     settings.POSTGRES_DB,
#     user=settings.POSTGRES_USER,
#     password=settings.POSTGRES_PASSWORD,
#     host=settings.DB_HOST,
#     port=settings.DB_PORT,
# )
db = SqliteDatabase(settings.POSTGRES_DB)