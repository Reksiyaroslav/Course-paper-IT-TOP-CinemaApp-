from app.service.base_service import Base_Service
from uuid import UUID
from fastapi.exceptions import HTTPException
from app.list.list_searhc import list_serach_date
from app.utils.comon import (
    is_fistname_lastname,
    validet_star_rating,
    validate_is_data_range,
)
from ..db.model.model_db import Actor
from app.repositories.actors_repositorie import ActorRepository


class ActorService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.actor_repo = ActorRepository(self.session)

    async def create_actor(self, data, name_title_value=None):
        if not await validate_is_data_range(data[list_serach_date[1]], "actor"):
            raise HTTPException(
                detail="Что не так сдадой рождения возможно не находится дипозоне  1945-2025",
                status_code=404,
            )
        elif not await validet_star_rating(data, "star"):
            raise HTTPException(
                detail="Что не так с оценкой возможно не находится в дипозоне 1 от 10",
                status_code=400,
            )
        elif not await is_fistname_lastname(Actor, self.actor_repo.session, data):
            raise HTTPException(detail="Такой актёр уже есть ", status_code=400)
        return await self.actor_repo.create_actor(data)

    async def update_actor(self, actor_id, data):
        data_fikeld = list_serach_date[1]
        star_filed = "actor"
        if data_fikeld in data and data[data_fikeld] is not None:
            if not await validate_is_data_range(data[list_serach_date[1]], "actor"):
                raise HTTPException(
                    detail="Что не так сдадой рождения возможно не находится дипозоне 2025  или 1945",
                    status_code=400,
                )
        if star_filed in data and data[star_filed] is not None:
            if not await validet_star_rating(data, "star"):
                raise HTTPException(
                    detail="Что не так с оценкой возможно не находится в дипозоне 1 от 7",
                    status_code=402,
                )
        if not await is_fistname_lastname(Actor, self.actor_repo.session, data):
            raise HTTPException(detail="Такой актёр уже есть ", status_code=400)
        return await self.actor_repo.update_actor(data=data, actor_id=actor_id)

    async def get_actor_list(self):
        return await self.actor_repo.get_actors()

    async def get_actor_by_id(self, actor_id):
        return await self.actor_repo.get_actor_by_id(actor_id=actor_id)

    async def delete_actor(self, actor_id):
        return await self.actor_repo.delete_actor(actor_id)

    async def get_fistname_lastname_pat(self, name: str):
        if not name or not name.strip():
            raise HTTPException(status_code=424, detail="Нет такой актера часть имени ")
        return await self.actor_repo.get_actorname(name.strip())

    async def get_serahc_name_list(self, name: str, limint: int):
        if not name or not name.strip():
            raise HTTPException(status_code=424, detail="Нет такой актера часть имени ")
        return await self.actor_repo.get_actorname_list(name.strip(), limint)
