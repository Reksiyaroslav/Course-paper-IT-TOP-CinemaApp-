from litestar import Litestar, get
from litestar.di import Provide

from app.handler.handler_film import FilmControlle
from app.handler.handler_user import UserControlle
from app.handler.handler_actor import ActorControlle
from app.handler.handler_author import AuthorControlle
from app.handler.handler_coment import ComentControlle
from app.handler.handler_ratingfilm import RatingFilmControlle
from app.utils.sricpt import seend_database
from app.db.engine import plugin, provide_async_session
from app.auth.auth import jwt_auth,AuthController,ProtectedController
from contextlib import asynccontextmanager
from typing import AsyncIterator
import uvicorn
@asynccontextmanager
async def lifespan(app:Litestar)->AsyncIterator[None]:
    await seend_database()
    yield
@get("/" ,security=[],include_in_schema=False)
async def hello_world() -> dict[str, str]:
    return {"hello": "world"}

dependencies={"async_session": Provide(provide_async_session ,sync_to_thread=False)}


app = Litestar(
    route_handlers=[hello_world,FilmControlle,UserControlle,ActorControlle,AuthorControlle,ComentControlle,RatingFilmControlle,AuthController,ProtectedController]
    ,plugins=[plugin],
    dependencies=dependencies
    ,debug=1,on_app_init=[jwt_auth.on_app_init]
    ,lifespan=[lifespan])
if __name__ == "__run__":

    uvicorn.run(app ,host="0.0.0.0",port=90)
