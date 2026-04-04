from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)
session_factory = async_sessionmaker(bind=engine)
