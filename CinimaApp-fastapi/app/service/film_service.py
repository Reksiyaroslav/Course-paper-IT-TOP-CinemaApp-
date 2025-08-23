from app.service.base_service import Base_Service
from app.utils.comon import is_name_title, validate_is_data_range, validet_star_rating
from app.list.list_searhc import (
    list_serach_date,
    list_serach_name_title,
    list_serach_rating,
)
from fastapi.exceptions import HTTPException
from uuid import UUID


class FilmService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)

    async def create_model(self, data, name_title_value=None):
        if await validate_is_data_range(data[list_serach_date[0]], "film"):
            if await validet_star_rating(data, list_serach_rating[1]):
                if not await is_name_title(
                    model=self.repo.model,
                    session=self.repo.session,
                    name_filed=list_serach_name_title[3],
                    name_or_title_value=data[list_serach_name_title[3]],
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="Фильм с таким названием есть уже существует",
                    )
                else:
                    data["path_image"] = "../images/cat.jpg"
                    return await super().create_model(data, name_title_value)
            else:
                raise HTTPException(
                    detail="Что не так с оценкой   возможно не находится в дипозоне 1 от 10",
                    status_code=400,
                )
        else:
            raise HTTPException(
                detail="Что не так с датой возможно ненаходится в дипозоне 1995 от 2025",
                status_code=400,
            )

    async def update_model(self, model_id, data):
        if await validate_is_data_range(data[list_serach_date[0]], "film"):
            if await validet_star_rating(data, list_serach_rating[1]):
                if not await is_name_title(
                    model=self.repo.model,
                    session=self.repo.session,
                    name_filed=list_serach_name_title[3],
                    name_or_title_value=data[list_serach_name_title[3]],
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="Фильм с таким названием есть уже существует",
                    )
                else:
                    return await super().update_model(model_id, data)
            else:
                raise HTTPException(
                    detail="Что не так с оценкой возможно не находится в дипозоне 1 от 10",
                    status_code=400,
                )
        else:
            raise HTTPException(
                detail="Что не так с датой  возможно ненаходится в дипозоне 1995 от 2025",
                status_code=400,
            )

    async def add_actors_film_model(self, film_id: UUID, actor_list: list[UUID]):
        return await self.repo.add_list_actor_id(actor_list, film_id)

    async def add_authors_film_model(self, film_id: UUID, author_list: list[UUID]):
        return await self.repo.add_list_author_id(author_list, film_id)

    async def get_film_titles(self, titles: str,limint:int):
        return await self.repo.get_films_title_list(titles,limint)

    async def get_film_title(self, title: str,limint:int):
        return await self.repo.get_film_title(title,limint)

    async def get_list_actor(self, film_id: UUID):
        return await self.repo.get_list_actor(film_id)

    async def get_list_author(self, film_id: UUID):
        return await self.repo.get_list_author(film_id)
