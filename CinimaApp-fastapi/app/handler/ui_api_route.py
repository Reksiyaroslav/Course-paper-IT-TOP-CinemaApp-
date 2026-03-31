from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter, Depends, Form
from typing import Optional
from uuid import UUID
from urllib.parse import urlencode
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
    get_country_service,
    CountryService,
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


@ui_router.post("/type_film_and_country/")
@ui_router.get("/type_film_and_country/")
async def show_type_film_country(
    request: Request,
    type_action: Optional[str] = "list",
    type_model: Optional[str] = None,
    message: Optional[str] = None,
    item_id: Optional[UUID] = None,
    film_service: FilmService = Depends(get_film_service),
    country_service: CountryService = Depends(get_country_service),
    user=Depends(get_curen_user),
):
    countys_relult = await country_service.get_countrys()
    types_film_relult = await film_service.get_types_film()
    types_film = types_film_relult.types_film
    countrys = countys_relult.countrys
    return teamlates.TemplateResponse(
        "type_film_and_countries.html",
        context={
            "request": request,
            "countrys": countrys,
            "types_film": types_film,
            "type_action": type_action,
            "type_model": type_model,
            "message": message,
            "item_id": item_id,
            "user": user,
        },
    )


@ui_router.post("/update_model/{env_type_model}/{item_id}/{err}")
@ui_router.get("/update_model/{env_type_model}/{item_id}")
async def update_model(
    request: Request,
    item_id: UUID,
    env_type_model: TypeModel,
    film_service: FilmService = Depends(get_film_service),
    actor_service: ActorService = Depends(get_actor_service),
    author_service: AuthorService = Depends(get_author_service),
    user_service: UserService = Depends(get_user_service),
    country_service: CountryService = Depends(get_country_service),
    err: str = "",
    user=Depends(get_curen_user),
):
    service = {
        TypeModel.Actor: actor_service.get_actor_by_id,
        TypeModel.Author: author_service.get_author_by_id,
        TypeModel.Film: film_service.get_film_by_id,
        TypeModel.User: user_service.get_user_by_id,
    }
    data = await service[env_type_model](item_id)
    if env_type_model == TypeModel.Film:
        authors_reult = await author_service.get_authors()
        actors_reult = await actor_service.get_actor_list()
        types_film_reult = await film_service.get_types_film()
        countrys_reult = await country_service.get_countrys()
        authors = authors_reult.author
        actors = actors_reult.actors
        types_film = types_film_reult.types_film
        countrys = countrys_reult.countrys
        return teamlates.TemplateResponse(
            "update_model.html",
            context={
                "request": request,
                "data": data,
                "model_id": item_id,
                "type_model": env_type_model.value,
                "authors": authors,
                "actors": actors,
                "types_film": types_film,
                "countrys": countrys,
                "err": err,
                "user": user,
            },
        )
    if env_type_model == TypeModel.Actor or env_type_model == TypeModel.Author:
        countrys_reult = await country_service.get_countrys()
        countrys = countrys_reult.countrys
        return teamlates.TemplateResponse(
            "update_model.html",
            context={
                "request": request,
                "data": data,
                "model_id": item_id,
                "type_model": env_type_model.value,
                "countrys": countrys,
                "err": err,
                "user": user,
            },
        )
    else:
        return teamlates.TemplateResponse(
            "update_model.html",
            context={
                "request": request,
                "data": data,
                "model_id": item_id,
                "type_model": env_type_model.value,
                "err": err,
                "user": user,
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


@ui_router.post(path="/main/{type_model}", name="main_item")
@ui_router.get(path="/main/{type_model}", name="main_item")
async def main_pages(
    request: Request,
    type_model: TypeModel,
    film_service: FilmService = Depends(get_film_service),
    actor_server: ActorService = Depends(dependency=get_actor_service),
    author_service: AuthorService = Depends(dependency=get_author_service),
    user=Depends(get_curen_user),
):
    actors = None
    films = None
    if type_model == TypeModel.Film:
        films_list = await film_service.get_film_block()
        films = films_list.films
        return teamlates.TemplateResponse(
            name="main.html",
            context={"request": request, "films": films, "actors": None, "user": user},
        )
    else:
        if type_model == TypeModel.Actor:
            relult = await actor_server.get_actor_list()
            actors = relult.actors
        if type_model == TypeModel.Author:
            relult = await author_service.get_authors()
            actors = relult.author
        return teamlates.TemplateResponse(
            name="main.html",
            context={"request": request, "actors": actors, "films": None, "user": user},
        )


@ui_router.post("/update_user_role/{err}/")
@ui_router.get("/update_user_role/")
async def update_form_role_user(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    user=Depends(get_curen_user),
    err: str = "",
):
    users_relult = await user_service.get_all_user()
    users = users_relult.user_list
    return teamlates.TemplateResponse(
        "update_role_user.html",
        context={"request": request, "user": user, "users": users, "err": err},
    )


@ui_router.post(path="/create_model/{type_model}/{err}", name="create_model")
@ui_router.get(path="/create_model/{type_model}", name="create_model")
async def create_model(
    request: Request,
    type_model: str,
    actor_service: ActorService = Depends(get_actor_service),
    author_service: AuthorService = Depends(get_author_service),
    film_service: FilmService = Depends(get_film_service),
    country_service: CountryService = Depends(get_country_service),
    err: str = "",
    user=Depends(get_curen_user),
):
    if type_model == "film":
        authors_reult = await author_service.get_authors()
        actors_reult = await actor_service.get_actor_list()
        types_film_reult = await film_service.get_types_film()
        countrys_reult = await country_service.get_countrys()
        authors = authors_reult.author
        actors = actors_reult.actors
        types_film = types_film_reult.types_film
        countrys = countrys_reult.countrys
        return teamlates.TemplateResponse(
            name="create_model.html",
            context={
                "request": request,
                "data": {},
                "actors": actors,
                "authors": authors,
                "types_film": types_film,
                "countrys": countrys,
                "type_model": type_model,
                "err": err,
                "user": user,
            },
        )
    if type_model == TypeModel.Actor.value or type_model == TypeModel.Author.value:
        countrys_relult = await country_service.get_countrys()
        countrys = countrys_relult.countrys
        return teamlates.TemplateResponse(
            name="create_model.html",
            context={
                "request": request,
                "data": {},
                "countrys": countrys,
                "type_model": type_model,
                "err": err,
            },
        )
    else:
        return teamlates.TemplateResponse(
            name="create_model.html",
            context={
                "request": request,
                "data": {},
                "type_model": type_model,
                "err": err,
            },
        )


@ui_router.post(path="/serarcht_item/")
async def serach_items(
    request: Request,
    search_text: str = Form(""),
    film_service: FilmService = Depends(get_film_service),
    actor_service: ActorService = Depends(get_actor_service),
    author_service: AuthorService = Depends(get_author_service),
    user=Depends(get_curen_user),
):
    films_relult = await film_service.get_film_titles(titles=search_text)
    actors_relult = await actor_service.get_serahc_name_list(search_text)
    authors_relult = await author_service.get_fistname_lastname_pat_list(search_text)
    films = films_relult.films
    actors = actors_relult.actors
    authors = authors_relult.author
    count_films: int = len(films)
    count_actors: int = len(actors)
    count_authors: int = len(authors)
    return teamlates.TemplateResponse(
        "relult_search.html",
        context={
            "request": request,
            "films": films,
            "actors": actors,
            "authors": authors,
            "search_text": search_text,
            "count_films": count_films,
            "count_actors": count_actors,
            "count_authors": count_authors,
            "user": user,
        },
    )
