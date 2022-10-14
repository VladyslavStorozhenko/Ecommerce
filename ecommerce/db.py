from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


engine = create_engine(f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}')

Session = sessionmaker(bind=engine)

Base = declarative_base()


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
