from litestar import Litestar, get,Response
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from app.handler.handler_film import FilmControlle
from app.handler.handler_user import UserControlle
from app.handler.handler_actor import ActorControlle
from app.handler.handler_author import AuthorControlle
from app.db.engine import plugin, provide_async_session
from app.auth.auth import jwt_auth,AuthController,ProtectedController
import uvicorn

@get("/" ,security=[])
async def hello_world() -> dict[str, str]:
    return {"hello": "world"}

dependencies={"async_session": Provide(provide_async_session ,sync_to_thread=False)}


app = Litestar(
    route_handlers=[hello_world,FilmControlle,UserControlle,ActorControlle,AuthorControlle,AuthController,ProtectedController]
    ,plugins=[plugin],
    dependencies=dependencies
    ,debug=1,on_app_init=[jwt_auth.on_app_init])
if __name__ == "__run__":

    uvicorn.run(app ,host="0.0.0.0",port=90)
