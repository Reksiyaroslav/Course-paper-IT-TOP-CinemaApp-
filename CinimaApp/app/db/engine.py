from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession,create_async_engine,async_sessionmaker
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig,SQLAlchemyPlugin
import os 
from dotenv import load_dotenv

load_dotenv()

DB_URL  = os.getenv("DB_URL")

engine = create_async_engine(DB_URL,echo=True)
async_session_factory = async_sessionmaker(engine,expire_on_commit=False)
sesion_confing = AsyncSessionConfig(expire_on_commit=False)

config = SQLAlchemyAsyncConfig(connection_string = DB_URL,session_config= sesion_confing,create_all = True)

plugin = SQLAlchemyPlugin(config=config)

async def provide_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()
