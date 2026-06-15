from logging import Logger

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import os
from dotenv import load_dotenv
from app.db.model.model_db import Base
from app.utils.loggin import get_login

load_dotenv()

DB_URL = os.getenv("DB_URL_DEV")
log: Logger = get_login(name=__name__)
enigine = create_async_engine(url=DB_URL, echo=True)

new_session = async_sessionmaker(enigine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        try:
            log.debug("созданые поток нове сеси")
            yield session
        finally:
            log.debug("закрыта сеси")
            await session.close()


async def create_tabel():
    async with enigine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) для удаление
        await conn.run_sync(Base.metadata.create_all)
