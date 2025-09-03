from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv
from app.db.model.model_db import Base

load_dotenv()

DB_URL = os.getenv("DB_URL_DEV")
enigine = create_async_engine(url=DB_URL, echo=True)

new_session = async_sessionmaker(enigine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tabel():
    async with enigine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) для удаление
        await conn.run_sync(Base.metadata.create_all)
