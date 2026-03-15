from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter, Depends
from uuid import UUID
from app.service.film_service import FilmService
from app.service.user_service import UserService
from app.service.actor_service import ActorService
from app.utils.depencines import get_actor_service, get_film_service, get_user_service
from app.enums.type_model import TypeModel


ui_router = APIRouter(prefix="/frondet", tags=["Визуал"])
teamlates = Jinja2Templates(directory="app/templates")


@ui_router.get("/profile/{env_type_mode}/{item_id}")
async def view_item(
    request: Request,
    item_id: UUID,
    env_type_mode: TypeModel,
    film_service: FilmService = Depends(get_film_service),
    actor_service: ActorService = Depends(get_actor_service),
    user_service: UserService = Depends(get_user_service),
) -> dict:
    service = {
        TypeModel.Actor: actor_service.get_actor_by_id,
        TypeModel.Film: film_service.get_film_by_id,
        TypeModel.User: user_service.get_user_by_id,
    }
    data = await service[env_type_mode](item_id)
    return teamlates.TemplateResponse(
        name="profiles.html", context={"request": request, "item": data}
    )

@ui_router.post(path="/reg", name="reg")
@ui_router.get(path="/reg", name="reg")
async def reg(request: Request):
    return teamlates.TemplateResponse(name="reg.html", context={"request": request})

@ui_router.post(path="/log", name="log")
@ui_router.get(path="/log", name="log")
async def log(request: Request):
    return teamlates.TemplateResponse(name="log.html", context={"request": request})

@ui_router.post(path="/main", name="main_film")
@ui_router.get(path="/main", name="main_film")
async def main_pages(request: Request, film_service:FilmService=Depends(get_film_service)):
    films_list = await film_service.get_film_block()
    films = films_list.films
    return teamlates.TemplateResponse(
        name="main.html", context={"request": request, "films": films}
    )


@ui_router.get(path="/main_actor", name="main_actor")
async def main_pages_actor(
    request: Request, actor_server: ActorService = Depends(get_actor_service)
):
    actors = await actor_server.get_actor_list()
    return teamlates.TemplateResponse(
        name="main.html", context={"request": request, "actors": actors}
    )
