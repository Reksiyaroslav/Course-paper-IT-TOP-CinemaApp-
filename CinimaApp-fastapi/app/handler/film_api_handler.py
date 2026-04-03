from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Dict, Optional
from uuid import UUID
from app.utils.depencines import get_film_service, FilmService
from app.handler.ui_api_route import teamlates
from app.utils.router_help import parse_data_or_none
from app.scheme.film.model_film import (
    FilmCreateRequest,
    FilmUpdateRequest,
    FilmResponse,
    datetime,
)
from app.enums.type_model import TypeModel

"""
Сдесь сделано api для фильмов 
методы:
create_film -создание фильма 
get_films - получение списка фильмов
get_film_and_film_id-получение фильма по id
get_actor_and_film - получение актеров которые снялись в фильме 
get_author_and_film- получени авторов которые сняли фильм
get_film_title - получени фильма по названию
get_film_titles - получение фильма по букве или слову (нужно переделать)
add_actor_film -добавление актеров в фильм
add_author_film- добавление автров в фильм
update_film_film_id-обновление фильма
delete_film_film_id-удаление фильма
"""
film_router = APIRouter(prefix="/film", tags=["Film"])


@film_router.post(path="/create_film", name="film_create", response_model=None)
async def create_film(
    request: Request,
    title: str = Form(None),
    description: str = Form(None),
    release_date: str = Form(),
    image: UploadFile = File(None),
    actor_ids: list[UUID] = Form(default=[]),
    author_ids: list[UUID] = Form(default=[]),
    types_id: list[UUID] = Form(default=[]),
    country_id: UUID = Form(default=None),
    film_sevice: FilmService = Depends(get_film_service),
) -> HTMLResponse | RedirectResponse:
    try:
        paring_date = parse_data_or_none(
            date_str=release_date, field_name="release_date"
        )
        if not paring_date:
            raise HTTPException(
                detail="Не могут быть пуcтым поля Дата релиза", status_code=400
            )
        if not title or not description:
            raise HTTPException(
                detail="Не могут быть пуcтыми полями название описание", status_code=400
            )
        if len(title.strip()) < 10 or len(title.strip()) > 1000:
            raise HTTPException(
                detail="Минимальное количество  10 и максимальное 1000 количество  сиволов  у название",
                status_code=400,
            )
        if len(description.strip()) < 10 or len(description.strip()) > 1000:
            raise HTTPException(
                detail="Минимальное количество  10 и максимальное 1000 количество сиволов описание",
                status_code=400,
            )
        data: FilmCreateRequest = FilmCreateRequest(
            title=title, description=description, release_date=paring_date
        )
        message = await film_sevice.create_film(data.model_dump(), image)
        if isinstance(message, FilmResponse):
            if actor_ids:
                await film_sevice.add_actors_film_model(
                    actor_list=actor_ids, film_id=message.film_id
                )
            if author_ids:
                await film_sevice.add_authors_film_model(
                    film_id=message.film_id, author_list=author_ids
                )
            if country_id:
                await film_sevice.add_country(
                    film_id=message.film_id, country_id=country_id
                )
            if types_id:
                await film_sevice.add_types_film(
                    film_id=message.film_id, types_film=types_id
                )
            url = request.url_for("main_item", type_model="film")
            return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("create_model", type_model="film", err=e.detail)
        return RedirectResponse(url=url)


@film_router.get("s/")
async def get_films(
    film_service: FilmService = Depends(get_film_service),
):
    films = await film_service.get_list_film()
    return films


@film_router.get("s_block/")
async def get_block_films(
    film_service: FilmService = Depends(get_film_service),
):
    films = await film_service.get_film_block()
    return films


@film_router.get("/profile/{film_id}")
async def get_film_and_film_id(
    film_id: UUID, film_service: FilmService = Depends(get_film_service)
):
    film = await film_service.get_film_by_id(film_id)
    return film


@film_router.get(
    "/get_type_model/{film_id}",
)
async def get_type_model_and_film(
    film_id: UUID,
    type_model: TypeModel,
    film_serveice: FilmService = Depends(get_film_service),
):
    model = await film_serveice.get_list_model(film_id, type_model)
    return model


@film_router.get("/update_rating/{film_id}")
async def update_rating(
    film_id: UUID, film_serveice: FilmService = Depends(get_film_service)
) -> Dict[str, str]:
    film = await film_serveice.update_rating(film_id)
    if isinstance(film, str):
        return {"message": film}
    else:
        return film


@film_router.get("/get_titles_film/{film_titles}")
async def get_film_titles(
    film_titles: str, film_service: FilmService = Depends(get_film_service)
):
    films = await film_service.get_film_titles(film_titles)
    return films


@film_router.put("/update/{film_id}/")
@film_router.post("/update/{film_id}/")
async def update_film(
    film_id: UUID,
    request: Request,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    release_date: Optional[str] = Form(None),
    image: UploadFile = File(None),
    actor_ids: Optional[list[UUID]] = Form(default=[]),
    author_ids: list[UUID] = Form(default=[]),
    types_id: list[UUID] = Form(default=[]),
    country_id: UUID = Form(default=None),
    film_service: FilmService = Depends(get_film_service),
):
    try:
        paring_date = parse_data_or_none(
            date_str=release_date, field_name="release_date"
        )
        if not paring_date:
            raise HTTPException(
                detail="Не могут быть пуcтым поля Дата релиза", status_code=400
            )
        if not title or not description:
            raise HTTPException(
                detail="Не могут быть пуcтыми полями название описание", status_code=400
            )
        if len(title.strip()) < 10 or len(title.strip()) > 1000:
            raise HTTPException(
                detail="Минимальное количество  10 и максимальное 1000 количество  сиволов  у название",
                status_code=400,
            )
        if len(description.strip()) < 10 or len(description.strip()) > 1000:
            raise HTTPException(
                detail="Минимальное количество  10 и максимальное 1000 количество сиволов описание",
                status_code=400,
            )
        data = FilmUpdateRequest(
            description=description, title=title, release_date=paring_date
        )
        await film_service.update_film(film_id, data.model_dump(), image=image)
        if actor_ids:
            await film_service.set_actors(film_id=film_id, actor_ids=actor_ids)
        if author_ids:
            await film_service.set_authors(film_id=film_id, author_ids=author_ids)
        if types_id:
            await film_service.set_types_film(film_id=film_id, types_film=types_id)
        if country_id:
            await film_service.set_country(film_id=film_id, country_id=country_id)
        url = request.url_for(
            "view_item", env_type_model=TypeModel.Film.value, item_id=film_id
        )
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for(
            "update_model", env_type_model="film", item_id=film_id, err=e.detail
        )
        return RedirectResponse(url)


@film_router.post("/add_authors_actors/{film_id}/")
async def add_authors_and_actors_film(
    film_id: UUID,
    actor_ids: list[UUID] = Form(default=None),
    author_ids: list[UUID] = Form(default=None),
    film_service: FilmService = Depends(get_film_service),
):
    if actor_ids:
        await film_service.add_actors_film_model(film_id=film_id, actor_list=actor_ids)
    if author_ids:
        await film_service.add_authors_film_model(
            film_id=film_id, author_list=author_ids
        )
    film = await film_service.get_film_by_id(film_id)
    return film


@film_router.post("/delete/{film_id}/")
@film_router.delete("/delete/{film_id}/")
async def delete_film(
    request: Request,
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service),
):
    try:
        await film_service.delete_film(film_id)
        url = request.url_for("main_item", type_model="film")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("view_item", env_type_model="film", item_id=film_id)
        return RedirectResponse(url)
