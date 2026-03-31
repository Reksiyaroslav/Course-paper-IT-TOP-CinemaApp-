from fastapi.exceptions import HTTPException
from uuid import UUID
from app.service.base_service import Base_Service
from app.enums.serach_fileld import SerachFiled
from app.enums.type_model import TypeModel
from app.utils.comon import (
    is_fistname_lastname,
    validet_star_rating,
    validate_is_data_range,
)
from ..db.model.model_db import Actor
from app.repositories.actors_repositorie import ActorRepository
from app.utils.noramliz_text import normalize_data, text_strip_lower
from app.scheme.actor.model_actor import (
    ActorListResponse,
    ActorResponse,
    Actor_FullResponse,
)


class ActorService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.actor_repo = ActorRepository(self.session)

    async def create_actor(self, data, name_title_value=None):
        print(data)
        filed_data = SerachFiled.Date.value[1]
        filed_rating = SerachFiled.Rating.value[0]
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.Actor.value)
        print(clean_data)
        if not await validate_is_data_range(
            clean_data.get(filed_data), TypeModel.Actor.value
        ):
            raise HTTPException(
                detail="Что не так сдадой рождения возможно не находится дипозоне  1945-2026",
                status_code=400,
            )
        elif not await validet_star_rating(data, filed_rating):
            raise HTTPException(
                detail="Что не так с оценкой возможно не находится в дипозоне 1 от 10",
                status_code=400,
            )
        elif not await is_fistname_lastname(Actor, self.actor_repo.session, clean_data):
            raise HTTPException(detail="Такой актёр уже есть ", status_code=400)
        new_actor = await self.actor_repo.create_actor(clean_data)
        if not new_actor:
            raise HTTPException(status_code=500, detail="Ошибка при создании актёра")
        return ActorResponse.from_orm(new_actor)

    async def update_actor(self, actor_id: UUID, data):
        filed_data = SerachFiled.Date.value[1]
        filed_rating = SerachFiled.Rating.value[0]
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.Actor.value)
        if filed_data in data and data[filed_data] is not None:
            if not await validate_is_data_range(
                data[filed_data], TypeModel.Actor.value
            ):
                raise HTTPException(
                    detail="Что не так сдадой рождения возможно не находится дипозоне 2025  или 1945",
                    status_code=400,
                )
        if filed_rating in data and data[filed_rating] is not None:
            if not await validet_star_rating(data, filed_rating):
                raise HTTPException(
                    detail="Что не так с оценкой возможно не находится в дипозоне 1 от 7",
                    status_code=402,
                )
        if not await is_fistname_lastname(Actor, self.actor_repo.session, clean_data):
            raise HTTPException(detail="Такой актёр уже есть ", status_code=400)
        update_actor = await self.actor_repo.update_actor(
            data=clean_data, actor_id=actor_id
        )
        if not update_actor:
            raise HTTPException(status_code=404, detail="Актёр не найден")
        return ActorResponse.from_orm(update_actor)

    async def get_actor_list(self):
        actors = await self.actor_repo.get_actors()
        return ActorListResponse(actors=actors)

    async def get_actor_by_id(self, actor_id: UUID):
        actor = await self.actor_repo.get_actor_by_id(actor_id=actor_id)
        if not actor:
            raise HTTPException(status_code=404, detail="Актёр не найден")
        return Actor_FullResponse.from_orm(actor)

    async def add_country(self, country_id: UUID, actor_id: UUID):
        actor = await self.actor_repo.add_country(
            actor_id=actor_id, country_id=country_id
        )
        if not actor:
            raise HTTPException(status_code=404, detail="Актёр не найден")
        return ActorResponse.from_orm(actor)

    async def set_country(self, country_id: UUID, actor_id: UUID):
        actor = await self.actor_repo.set_country(
            actor_id=actor_id, country_id=country_id
        )
        if not actor:
            raise HTTPException(status_code=404, detail="Актёр не найден")
        return ActorResponse.from_orm(actor)

    async def delete_actor(self, actor_id):
        success = await self.actor_repo.delete_actor(actor_id)
        if not success:
            raise HTTPException(status_code=404, detail="Актёр не найден")
        return {"message": "Актёр успешно удалён"}

    async def get_serahc_name_list(self, name: str):
        clear_name = text_strip_lower(name)
        actors = await self.actor_repo.get_actorname_list(clear_name)
        print(clear_name)
        if not actors:
            return ActorListResponse(actors=[])
        return ActorListResponse(actors=actors)
