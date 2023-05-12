from dataclasses import dataclass
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@dataclass
class Settings:
    DB_HOST: str = config("DB_HOST")
    DB_USER: str = config("DB_USER")
    DB_PASSWORD: str = config("DB_PASSWORD")
    DB_NAME: str = config("DB_NAME")
    DB_PORT: int = 5433
    
    def get_database_url(self)-> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()

engine = create_engine(settings.get_database_url())

SessionFactory = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)