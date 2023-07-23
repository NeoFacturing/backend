import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker

from app.database.config import settings

engine = create_engine(settings.DATABASE_URL(), pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@sqlalchemy.orm.as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
