from fastapi import APIRouter, Depends, HTTPException, status
from app.service.film_service import FilmService
from app.repositories.films_repositorie import FilmRepository
from app.scheme.model_actor import ActorResponse
from app.scheme.model_author import AuthorResponse
from app.scheme.model_film import (
    FilmCreateRequest,
    FilmResponse,
    FilmUpdateRequest,
    AddActorFilsmResponse,
    AddAuthorFilsmResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import get_session
from app.service.factory import get_service
from typing import List, Dict
from uuid import UUID
from app.utils.comon import SessionDep
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


@film_router.post("/")
async def create_film(
    data: FilmCreateRequest, async_session: SessionDep 
) -> FilmResponse:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    film = await film_servise.create_model(data.dict())
    return FilmResponse.from_orm(film)


@film_router.get("s/")
async def get_films(
    async_session: SessionDep ,
) -> List[FilmResponse]:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    films = await film_servise.get_models()
    return [FilmResponse.from_orm(film) for film in films]


@film_router.get("/{film_id}")
async def get_film_and_film_id(
    film_id: UUID, async_session: SessionDep 
) -> FilmResponse:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    film = await film_servise.get_model(film_id)
    return FilmResponse.from_orm(film)


@film_router.get("/get_actors/{film_id}")
async def get_actor_and_film(
    film_id: UUID, async_session: SessionDep 
) -> List[ActorResponse]:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    actors = await film_servise.get_list_actor(film_id)
    return [ActorResponse.from_orm(actor) for actor in actors ]


@film_router.get("/get_authors/{film_id}")
async def get_author_and_film(
    film_id: UUID, async_session: SessionDep 
) -> List[AuthorResponse]:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    authors = await film_servise.get_list_author(film_id)
    return [AuthorResponse.from_orm(author) for  author in authors ]


@film_router.get("/get_title_film/{film_title}")
async def get_film_title(
    film_title: str, async_session: SessionDep 
) -> FilmResponse:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    film = await film_servise.get_film_title(film_title)
    if not film:
        raise HTTPException(
            detail="Нету такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return FilmResponse.from_orm(film)


@film_router.get("/get_titles_film/{film_titles}")
async def get_film_titles(
    film_titles: str, async_session: SessionDep 
) -> List[FilmResponse]:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    films = await film_servise.get_film_titles(film_titles)
    if not films:
        raise HTTPException(
            detail="Нету такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return [FilmResponse.from_orm(film) for film in films]


@film_router.put("/update/{film_id}/")
async def update_film_film_id(
    film_id: UUID,
    data: FilmUpdateRequest,
    async_session: SessionDep ,
) -> FilmResponse:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    film = await film_servise.update_model(film_id, data.actor_ids)
    if not film:
        raise HTTPException(
            detail="Нету такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return FilmResponse.from_orm(film)


@film_router.post("/add_actor/{film_id}/")
async def add_actor_film(
    film_id: UUID,
    data: AddActorFilsmResponse,
    async_session: SessionDep ,
) -> FilmResponse:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    film = await film_servise.add_actors_film_model(film_id, data.actor_ids)
    if not film:
        raise HTTPException(
            detail="Нету такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return FilmResponse.from_orm(film)


@film_router.post("/add_author/{film_id}/")
async def add_author_film(
    film_id: UUID,
    data: AddAuthorFilsmResponse,
    async_session: SessionDep ,
) -> FilmResponse:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    film = await film_servise.add_author_film_model(film_id, data.dict())
    if not film:
        raise HTTPException(
            detail="Нету такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return FilmResponse.from_orm(film)


@film_router.delete("/delete/{film_id}/")
async def delete_film_film_id(
    film_id: UUID, async_session: SessionDep 
) -> Dict[str, str]:
    film_servise = await get_service(FilmService, FilmRepository, async_session)
    film = await film_servise.delete_model(film_id)
    if not film:
        raise HTTPException(
            detail="Нету такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return {"message": "Delete film and db"}
