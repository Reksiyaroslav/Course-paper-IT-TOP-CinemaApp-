from fastapi.exceptions import HTTPException
from fastapi import UploadFile
from uuid import UUID
from ..db.model.model_db import Film
from app.service.base_service import Base_Service
from app.enums.serach_fileld import SerachFiled
from app.enums.type_model import TypeModel
from app.utils.noramliz_text import normalize_data, text_strip_lower
from app.scheme.actor.model_actor import ActorListResponse
from app.scheme.author.model_author import AuthorlListResponse
from app.scheme.rating.model_ratingfilms import RatingFilmList
from app.scheme.comment.model_coment import ComentResponse
from app.scheme.film.model_film import (
    FilmResponse,
    FilmlListBlockResponse,
    FilmBaseList,
)
from app.scheme.film.type_film import TypeFilmResponse, ListTypeFilmResponse
from app.repositories.films_repositorie import FilmRepository
from app.repositories.type_film_repositorie import TypeFilmReposit
from app.repositories.ratingfilm_repositore import (
    RatingFilmRepository,
    RatingFilm as rating_model,
)
from app.utils.comon import is_name_title, validate_is_data_range, len_fields
from app.utils.upload_file import uplodat_file, delete_file


class FilmService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.film_repo: FilmRepository = FilmRepository(self.session)
        self.rating_repo: RatingFilmRepository = RatingFilmRepository(self.session)
        self.type_film_repo: TypeFilmReposit = TypeFilmReposit(self.session)

    async def create_film(
        self, data: dict, image: UploadFile, name_title_value=None
    ) -> FilmResponse:
        for key, value in data.items():
            len_fields(value, key)
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.Film.value)
        filed_name = SerachFiled.Name.value[3]
        filed_date = SerachFiled.Date.value[0]
        if not await validate_is_data_range(data[filed_date], TypeModel.Film.value):
            raise HTTPException(
                detail="Что не так с датой  возможно ненаходится в дипозоне от 1995-2025",
                status_code=400,
            )
        elif not await is_name_title(
            model=Film,
            session=self.film_repo.session,
            name_filed=filed_name,
            name_or_title_value=data[filed_name],
        ):
            raise HTTPException(
                status_code=409,
                detail="Фильм с таким названием есть уже существует",
            )
        if image and image.filename:
            image_file_path = await uplodat_file(image, clean_data.get("title"))
            clean_data["path_image"] = image_file_path
        else:
            clean_data["path_image"] = "images/cat.jpg"
        new_film = await self.film_repo.create_film(clean_data)
        if not new_film:
            raise HTTPException(status_code=500, detail="Ошибка при создании фильма")
        film = await self.get_film_by_id(film_id=new_film.film_id)
        return film

    async def create_type_film(self, data: dict):
        for key, value in data.items():
            len_fields(value, key)

        clean_data = normalize_data(data=data, model_type=TypeModel.TypeFilm.value)
        name_type_film = data.get("type_film_name")
        if await self.type_film_repo.is_double_not(name_type_film=name_type_film):
            raise HTTPException(
                detail="Найден дубликат нельзя создавать с таким именем",
                status_code=408,
            )
        new_type_film = await self.type_film_repo.create_type_film(data=clean_data)
        if not new_type_film:
            raise HTTPException(
                status_code=500, detail="Ошибка при создании типа фильма"
            )

        return TypeFilmResponse.from_orm(new_type_film)

    async def get_types_film(self):
        types_film = await self.type_film_repo.get_types_film()
        return ListTypeFilmResponse(types_film=types_film)

    async def get_type_film_by_id(self, type_film_id):
        type_film = await self.type_film_repo.get_type_film_by_id(type_film_id)
        if not type_film:
            raise HTTPException(
                detail="Нет типа  с таким id",
                status_code=404,
            )
        return TypeFilmResponse.from_orm(type_film)

    async def update_type_film(self, data, type_film_id):
        for key, value in data.items():
            len_fields(value, key)
        clean_data = normalize_data(data=data, model_type=TypeModel.TypeFilm.value)
        name_type_film = data.get("type_film_name")
        if await self.type_film_repo.update_is_double_not(
            type_film_id=type_film_id, name_type_film=name_type_film
        ):
            raise HTTPException(
                detail="Найден дубликат нельзя создавать с таким именем",
                status_code=408,
            )
        update_type_film = await self.type_film_repo.update_type_film(
            data=clean_data, type_film_id=type_film_id
        )
        return TypeFilmResponse.from_orm(update_type_film)

    async def delete_type_film(self, type_film_id):
        await self.type_film_repo.delete_type_film(type_film_id=type_film_id)
        return {"detail": "Удалили"}

    async def get_film_by_id(self, film_id):
        film = await self.film_repo.get_film_by_id(film_id)
        if not film:
            raise HTTPException(
                detail="Нет фильма с таким id ",
                status_code=404,
            )
        return FilmResponse.from_orm(film)

    async def get_list_film(self):
        films = await self.film_repo.get_films()
        return FilmBaseList(films=films)

    async def update_film(self, film_id, data, image: UploadFile):
        for key, value in data.items():
            len_fields(value, key)
        clean_data: dict = normalize_data(
            data=data, model_type=TypeModel.TypeFilm.value
        )
        title = clean_data.get("title")
        filed_name = SerachFiled.Name.value[3]
        filed_date = SerachFiled.Date.value[0]
        if not await validate_is_data_range(
            clean_data[filed_date], TypeModel.Film.value
        ):
            raise HTTPException(
                detail="Что не так с датой  возможно ненаходится в дипозоне от 1995-2025",
                status_code=400,
            )
        elif await self.film_repo.get_doble_title(film_id=film_id, title=title):

            raise HTTPException(
                status_code=409,
                detail="Фильм с таким названием есть уже существует",
            )
        curent_film = await self.get_film_by_id(film_id=film_id)
        if not curent_film:
            raise HTTPException(
                status_code=409,
                detail="Фильм с таким названием есть уже существует",
            )
        if image and image.filename:
            image_pat = curent_film.path_image
            if image_pat:
                if image_pat != "images/cat.jpg":
                    await delete_file(image_pat)
                image_file_path = await uplodat_file(image, title)
                clean_data["path_image"] = image_file_path

        update_film = await self.film_repo.update_film(film_id=film_id, data=clean_data)
        if not update_film:
            raise HTTPException(status_code=500, detail="Ошибка при обновлении фильма")
        return FilmResponse.from_orm(update_film)

    async def delete_film(self, film_id):
        film_remove = await self.get_film_by_id(film_id)
        image_pat = film_remove.path_image
        if image_pat:
            await delete_file(image_pat)
        boolen_reposnes = await self.film_repo.delete_film(film_id)
        if not boolen_reposnes:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return {"message": "Фильм успешно удалён"}

    async def update_rating(self, film_id):
        avg_rating = await self.rating_repo.average_rating_film(film_id)
        update_film = await self.film_repo.update_rating(
            avg_rating=avg_rating, film_id=film_id
        )
        if not update_film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(update_film)

    async def add_country(self, film_id: UUID, country_id: UUID):
        film = await self.film_repo.add_country(country_id=country_id, film_id=film_id)
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def add_actors_film_model(self, film_id: UUID, actor_list: list[UUID]):
        film = await self.film_repo.add_list_actor_id(
            actor_ids=actor_list, film_id=film_id
        )
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def add_authors_film_model(self, film_id: UUID, author_list: list[UUID]):
        film = await self.film_repo.add_list_author_id(
            author_ids=author_list, film_id=film_id
        )
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def add_types_film(self, film_id: UUID, types_film: list[UUID]):
        film = await self.film_repo.add_types_film(
            types_film_id=types_film, film_id=film_id
        )
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def set_types_film(self, film_id: UUID, types_film: list[UUID]):
        film = await self.film_repo.set_type_film(
            types_film_id=types_film, film_id=film_id
        )
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def set_actors(self, film_id: UUID, actor_ids: list[UUID]):
        film = await self.film_repo.set_actors(actors_id=actor_ids, film_id=film_id)
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def set_authors(self, film_id: UUID, author_ids: list[UUID]):
        film = await self.film_repo.set_auhtors(authors_id=author_ids, film_id=film_id)
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def set_country(self, film_id: UUID, country_id: UUID):
        film = await self.film_repo.set_country(country_id=country_id, film_id=film_id)
        if not film:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return FilmResponse.from_orm(film)

    async def get_film_block(self):
        films_block = await self.film_repo.get_film_block()
        return FilmlListBlockResponse(films=films_block)

    async def get_film_titles(self, titles: str):
        serach_text = text_strip_lower(text=titles)
        films = await self.film_repo.get_film_title(serach_text)
        if not films:
            return FilmBaseList(films=[])
        return FilmBaseList(films=films)

    async def get_list_model(self, film_id: UUID, type_model_list: TypeModel):
        if type_model_list == TypeModel.Rating:
            ratings = await self.film_repo.get_list_rating(film_id)
            return RatingFilmList(rating_list=ratings)
        if type_model_list == TypeModel.Comment:
            comments = await self.film_repo.get_list_coment(film_id)
            return [ComentResponse.from_orm(comment) for comment in comments]
        if type_model_list == TypeModel.Actor:
            actors = await self.film_repo.get_list_actor(film_id)
            return ActorListResponse(actors=actors)
        if type_model_list == TypeModel.Author:
            authors = await self.film_repo.get_list_author(film_id)
            return AuthorlListResponse(author=authors)
        else:
            raise HTTPException(
                status_code=400,
                detail="Не надено по модеям  есть только rating ,coment,actor,author",
            )

    async def get_serach_profile(
        self,
        min_rating: float = None,
        max_rating: float = None,
        country_name: str = None,
        types_film: list[str] = None,
        min_date=None,
        max_date=None,
    ):
        if (
            min_rating == 0.0
            and max_rating == 0.0
            and not country_name
            and not types_film
            and not min_date
            and not max_date
        ):
            films = await self.get_list_film()
            if not films:
                raise HTTPException(status_code=400, detail="База пустая")
            return films
        films = await self.film_repo.get_film_ratings_date_country_type_film(
            min_rating=min_rating,
            max_rating=max_rating,
            country_name=country_name,
            type_film=types_film,
            min_date=min_date,
            max_date=max_date,
        )
        return FilmBaseList(films=films)

    # async def get_list_actor(self, film_id: UUID):
    #     return await self.film_repo.get_list_actor(film_id)

    # async def get_list_author(self, film_id: UUID):
    #     return await self.film_repo.get_list_author(film_id)

    # async def get_list_coment(self, film_id: UUID):
    #     return await self.film_repo.get_list_coment(film_id)

    # async def get_list_rating(self, film_id: UUID):
    #     return await self.film_repo.get_list_rating(film_id)
