from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str = "db"
    DB_PORT: int = 5432

    class Config:
        env_file = ".env"


settings = Settings()
