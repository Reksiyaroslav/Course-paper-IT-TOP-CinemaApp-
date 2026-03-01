from app.repositories.films_repositorie import FilmRepository
from app.repositories.ratingfilm_repositore import RatingFilmRepository
from app.utils.comon import is_name_title, validate_is_data_range, validet_star_rating
from app.list.list_searhc import (
    list_serach_date,
    list_serach_name_title,
    list_serach_rating,
    list_type_model,
)
from fastapi.exceptions import HTTPException
from uuid import UUID
from ..db.model.model_db import Film
from app.service.base_service import Base_Service


class FilmService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.film_repo: FilmRepository = FilmRepository(self.session)
        self.rating_repo = RatingFilmRepository(self.session)

    async def create_film(self, data, name_title_value=None):
        if not await validate_is_data_range(data[list_serach_date[0]], "film"):
            raise HTTPException(
                detail="Что не так с датой  возможно ненаходится в дипозоне от 1995-2025",
                status_code=400,
            )
        elif not await is_name_title(
            model=Film,
            session=self.film_repo.session,
            name_filed=list_serach_name_title[3],
            name_or_title_value=data[list_serach_name_title[3]],
        ):
            raise HTTPException(
                status_code=409,
                detail="Фильм с таким названием есть уже существует",
            )

        data["path_image"] = "images/cat.jpg"
        return await self.film_repo.create_film(data)

    async def get_film_by_id(self, film_id):
        return await self.film_repo.get_film_by_id(film_id)

    async def get_list_film(self):
        return await self.film_repo.get_films()

    async def update_film(self, film_id, data):
        if not await validate_is_data_range(data[list_serach_date[0]], "film"):
            raise HTTPException(
                detail="Что не так с датой  возможно ненаходится в дипозоне от 1995-2025",
                status_code=400,
            )
        elif not await is_name_title(
            model=Film,
            session=self.film_repo.session,
            name_filed=list_serach_name_title[3],
            name_or_title_value=data[list_serach_name_title[3]],
        ):
            raise HTTPException(
                status_code=409,
                detail="Фильм с таким названием есть уже существует",
            )
        return await self.film_repo.update_film(film_id=film_id, data=data)

    async def delete_film(self, film_id):
        return await self.film_repo.delete_film(film_id)

    async def update_rating(self, film_id):
        avg_rating = await self.rating_repo.average_rating_film(film_id)
        return await self.film_repo.update_rating(
            avg_rating=avg_rating, film_id=film_id
        )

    async def add_actors_film_model(self, film_id: UUID, actor_list: list[UUID]):
        return await self.film_repo.add_list_actor_id(
            actor_list=actor_list, film_id=film_id
        )

    async def add_authors_film_model(self, film_id: UUID, author_list: list[UUID]):
        return await self.film_repo.add_list_author_id(
            author_ids=author_list, film_id=film_id
        )

    async def get_film_block(self):
        return await self.film_repo.get_film_block()

    async def get_film_titles(self, titles: str, limint: int):
        return await self.film_repo.get_films_title_list(titles, limint)

    async def get_film_title(self, title: str, limint: int):
        return await self.film_repo.get_film_title(title, limint)

    async def get_list_model(self, film_id: UUID, type_model_list: str):
        if type_model_list == list_type_model[0]:
            return await self.film_repo.get_list_rating(film_id)
        if type_model_list == list_type_model[1]:
            return await self.film_repo.get_list_coment(film_id)
        if type_model_list == list_type_model[2]:
            return await self.film_repo.get_list_actor(film_id)
        if type_model_list == list_type_model[3]:
            return await self.film_repo.get_list_author(film_id)
        else:
            raise HTTPException(
                status_code=404,
                detail="Не надено по модеям  есть только rating ,coment,actor,author",
            )

    # async def get_list_actor(self, film_id: UUID):
    #     return await self.film_repo.get_list_actor(film_id)

    # async def get_list_author(self, film_id: UUID):
    #     return await self.film_repo.get_list_author(film_id)

    # async def get_list_coment(self, film_id: UUID):
    #     return await self.film_repo.get_list_coment(film_id)

    # async def get_list_rating(self, film_id: UUID):
    #     return await self.film_repo.get_list_rating(film_id)
