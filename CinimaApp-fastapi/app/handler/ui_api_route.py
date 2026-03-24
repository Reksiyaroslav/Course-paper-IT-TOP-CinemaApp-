from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter, Depends
from uuid import UUID
from app.utils.depencines import (
    get_actor_service,
    get_film_service,
    get_user_service,
    get_author_service,
    get_rating_service,
    RatingFilmService,
    ActorService,
    UserService,
    AuthorService,
    FilmService,
)
from app.enums.type_model import TypeModel
from app.utils.router_help import get_curen_user


ui_router = APIRouter(prefix="/frondet", tags=["Визуал"])
teamlates = Jinja2Templates(directory="app/templates")


@ui_router.post("/profile/{env_type_model}/{item_id}")
@ui_router.get("/profile/{env_type_model}/{item_id}")
async def view_item(
    request: Request,
    item_id: UUID,
    env_type_model: TypeModel,
    film_service: FilmService = Depends(get_film_service),
    actor_service: ActorService = Depends(get_actor_service),
    user_service: UserService = Depends(get_user_service),
    author_service: AuthorService = Depends(get_author_service),
    ratting_service: RatingFilmService = Depends(get_rating_service),
    user=Depends(get_curen_user),
) -> dict:
    service = {
        TypeModel.Actor: actor_service.get_actor_by_id,
        TypeModel.Film: film_service.get_film_by_id,
        TypeModel.User: user_service.get_user_by_id,
        TypeModel.Author: author_service.get_author_by_id,
    }
    rating_user = None
    data = await service[env_type_model](item_id)
    if user and env_type_model.value == "film":
        rating_user = await ratting_service.get_by_user_id_and_film_id(
            user_id=user.user_id, film_id=item_id
        )

    return teamlates.TemplateResponse(
        name="profiles.html",
        context={
            "request": request,
            "item": data,
            "item_id": item_id,
            "user": user,
            "rating_user": rating_user,
        },
    )


@ui_router.post("/update_model/{env_type_model}/{item_id}")
@ui_router.get("/update_model/{env_type_model}/{item_id}")
async def update_model(
    request: Request,
    item_id: UUID,
    env_type_model: TypeModel,
    film_service: FilmService = Depends(get_film_service),
    actor_service: ActorService = Depends(get_actor_service),
    author_service: AuthorService = Depends(get_author_service),
    user_service: UserService = Depends(get_user_service),
):
    service = {
        TypeModel.Actor: actor_service.get_actor_by_id,
        TypeModel.Author: author_service.get_author_by_id,
        TypeModel.Film: film_service.get_film_by_id,
        TypeModel.User: user_service.get_user_by_id,
    }
    data = await service[env_type_model](item_id)
    return teamlates.TemplateResponse(
        "update_model.html",
        context={
            "request": request,
            "data": data,
            "model_id": item_id,
            "type_model": env_type_model.value,
            "err": "",
        },
    )


@ui_router.post(path="/reg", name="reg")
@ui_router.get(path="/reg", name="reg")
async def reg(request: Request):
    return teamlates.TemplateResponse(name="reg.html", context={"request": request})


@ui_router.post(path="/log", name="log")
@ui_router.get(path="/log", name="log")
async def log(request: Request):
    return teamlates.TemplateResponse(name="log.html", context={"request": request})


@ui_router.delete(path="/main", name="/main_film")
@ui_router.post(path="/main", name="main_film")
@ui_router.get(path="/main", name="main_film")
async def main_pages(
    request: Request,
    film_service: FilmService = Depends(get_film_service),
    user=Depends(get_curen_user),
):
    films_list = await film_service.get_film_block()
    films = films_list.films
    return teamlates.TemplateResponse(
        name="main.html", context={"request": request, "films": films, "user": user}
    )


@ui_router.post(path="/create_model/{type_model}", name="create_model")
@ui_router.get(path="/create_model/{type_model}", name="create_model")
async def create_model(
    request: Request,
    type_model: str,
    actor_service: ActorService = Depends(get_actor_service),
    author_service: AuthorService = Depends(get_author_service),
):
    if type_model == "film":
        authors = await author_service.get_authors()
        actors = await actor_service.get_actor_list()
        return teamlates.TemplateResponse(
            name="create_model.html",
            context={
                "request": request,
                "data": {},
                "actors": actors.actors,
                "authors": authors.author,
                "type_model": type_model,
            },
        )
    else:
        return teamlates.TemplateResponse(
            name="create_model.html",
            context={"request": request, "data": {}, "type_model": type_model},
        )


@ui_router.delete(path="/main_actor", name="/main_actor")
@ui_router.put(path="/main_actor", name="main_actor")
@ui_router.post(path="/main_actor", name="main_actor")
@ui_router.get(path="/main_actor", name="main_actor")
async def main_pages_actor(
    request: Request,
    actor_server: ActorService = Depends(get_actor_service),
    user=Depends(get_curen_user),
):
    relult = await actor_server.get_actor_list()
    actors = relult.actors

    return teamlates.TemplateResponse(
        name="main.html", context={"request": request, "actors": actors, "user": user}
    )


@ui_router.delete(path="/main_author", name="/main_author")
@ui_router.put(path="/main_author", name="/main_author")
@ui_router.post(path="/main_author", name="main_author")
@ui_router.get(path="/main_author", name="main_author")
async def main_pages_author(
    request: Request,
    author_server: AuthorService = Depends(dependency=get_author_service),
    user=Depends(get_curen_user),
):
    relult = await author_server.get_authors()
    authors = relult.author

    return teamlates.TemplateResponse(
        name="main.html", context={"request": request, "actors": authors, "user": user}
    )
