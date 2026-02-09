from fastapi import APIRouter, Depends, HTTPException, status
from app.scheme.model_actor import ActorResponse
from app.scheme.model_author import AuthorResponse
from app.scheme.model_ratingfilms import RatingFilmResponse
from app.scheme.model_coment import ComentResponse
from app.scheme.model_film import (
    FilmCreateRequest,
    FilmResponse,
    FilmUpdateRequest,
    AddActorFilsmResponse,
    AddAuthorFilsmResponse,
    FilmResponseBlocFilm,
)
from typing import List, Dict
from uuid import UUID
from app.utils.depencines import get_film_service ,FilmService

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
    data: FilmCreateRequest, film_sevice:FilmService =Depends(get_film_service)
) -> Dict:
    message = await film_sevice.create_film(data.dict())
    return message


@film_router.get("s/")
async def get_films(
   film_service:FilmService = Depends(get_film_service),
) -> List[FilmResponse]:
    films = await film_service.get_list_film()
    return [FilmResponse.from_orm(film) for film in films]
@film_router.get("s_block/")
async def get_block_films(
   film_service:FilmService = Depends(get_film_service),
) -> List[FilmResponseBlocFilm]:
    films = await film_service.get_film_block()
    return [FilmResponseBlocFilm.from_orm(film) for film in films]

@film_router.get("/{film_id}")
async def get_film_and_film_id(
    film_id: UUID, film_service:FilmService =Depends(get_film_service)
) -> FilmResponse:
    film = await film_service.get_film_by_id(film_id)
    return FilmResponse.from_orm(film)


@film_router.get("/get_type_model/{film_id}", response_model=List[ActorResponse| RatingFilmResponse| AuthorResponse|ComentResponse])
async def get_type_model_and_film(
    film_id: UUID, type_model:str,film_serveice:FilmService =Depends(get_film_service)
) :
    type_model = await film_serveice.get_list_model(film_id,type_model)
    if type_model == None:
        raise HTTPException(status_code= 404,detail="Not found type model")
    return type_model

@film_router.get("/update_rating/{film_id}")
async def update_rating(
    film_id: UUID, film_serveice:FilmService =Depends(get_film_service)
) -> FilmResponse|Dict[str,str]:
    film = await film_serveice.update_rating(film_id)
    if isinstance(film,str):
        return {"message":film}
    else:
        return FilmResponse.from_orm(film)

@film_router.get("/get_titles_film/{film_titles}")
async def get_film_titles(
    film_titles: str, film_service:FilmService = Depends(get_film_service)
) -> List[FilmResponse]:
    films = await film_service.get_film_titles(film_titles,5)
    if not films:
        raise HTTPException(
            detail="Нет такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return [FilmResponse.from_orm(film) for film in films]


@film_router.put("/update/{film_id}/")
async def update_film_film_id(
    film_id: UUID,
    data: FilmUpdateRequest,
    film_service:FilmService = Depends(get_film_service),
) -> FilmResponse:
    film = await film_service.update_film(film_id, data.dict())
    if not film:
        raise HTTPException(
            detail="Нет такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return FilmResponse.from_orm(film)


@film_router.post("/add_actor/{film_id}/")
async def add_actor_film(
    film_id: UUID,
    data: AddActorFilsmResponse,
    film_service:FilmService = Depends(get_film_service),
) -> FilmResponse:
    film = await film_service.add_actors_film_model(film_id, data.actor_ids)
    if not film:
        raise HTTPException(
            detail="Нет такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return FilmResponse.from_orm(film)


@film_router.post("/add_author/{film_id}/")
async def add_author_film(
    film_id: UUID,
    data: AddAuthorFilsmResponse,
   film_service:FilmService = Depends(get_film_service),
) -> FilmResponse:
    film = await film_service.add_authors_film_model(film_id, data.dict())
    if not film:
        raise HTTPException(
            detail="Нет такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return FilmResponse.from_orm(film)


@film_router.delete("/delete/{film_id}/")
async def delete_film_film_id(
    film_id: UUID, film_service:FilmService = Depends(get_film_service)
) -> Dict[str, str]:
    film = await film_service.delete_film(film_id)
    if not film:
        raise HTTPException(
            detail="Нет такого фильма ", status_code=status.HTTP_404_NOT_FOUND
        )
    return {"message": "Delete film and db"}
