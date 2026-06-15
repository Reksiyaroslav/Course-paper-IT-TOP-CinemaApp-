from fastapi.exceptions import HTTPException
from fastapi import UploadFile
from uuid import UUID
from app.service.base_service import Base_Service
from app.enums.serach_fileld import SerachFiled
from app.enums.type_model import TypeModel
from app.utils.comon import (
    is_fistname_lastname,
    validet_star_rating,
    validate_is_data_range,
    len_fields,
)
from app.utils.upload_file import delete_file,uplodat_file_image_film_and_peplo
from ..db.model.model_db import Actor
from app.repositories.actors_repositorie import ActorRepository,limit_people
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

    async def create_actor(self, data: dict, image:UploadFile,name_title_value=None):
            filed_data = SerachFiled.Date.value[1]
            filed_rating = SerachFiled.Rating.value[0]
            for key, value in data.items():
                len_fields(value, key)
            clean_data: dict = normalize_data(data=data, model_type=TypeModel.Actor.value)
            sus = clean_data.get(filed_data)
            if sus:
                if not await validate_is_data_range(
                    clean_data.get(filed_data), TypeModel.Actor.value
                ):
                    raise HTTPException(
                        detail="Что не так сдадой рождения возможно не находится дипозоне  1925-2026",
                        status_code=400,
                    )
            elif not await validet_star_rating(data, filed_rating):
                raise HTTPException(
                    detail="Что не так с оценкой возможно не находится в дипозоне 1 от 10",
                    status_code=400,
                )
            elif not await is_fistname_lastname(Actor, self.actor_repo.session, clean_data):
                raise HTTPException(detail="Такой актёр уже есть ", status_code=400)
            if image and image.filename:
                fistname:str = clean_data.get("fistname")
                lastname:str  = clean_data.get("lastname")
                fi = f"{lastname}_{fistname}"
                file_name = await uplodat_file_image_film_and_peplo(image,fi,type_model="peoples")
                clean_data["path_image"] = file_name
            else:
                clean_data["path_image"] ="images/cat.jpg"
            new_actor = await self.actor_repo.create_actor(clean_data)
            if not new_actor:
                raise HTTPException(status_code=500, detail="Ошибка при создании актёра")
            return ActorResponse.from_orm(new_actor)
        

    async def update_actor(self, actor_id: UUID, data:dict,image:UploadFile):
        filed_data = SerachFiled.Date.value[1]
        filed_rating = SerachFiled.Rating.value[0]
        for key, value in data.items():
            len_fields(value, key)
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.Actor.value)
        if filed_data in data and data[filed_data] is not None:
            if not await validate_is_data_range(
                data[filed_data], TypeModel.Actor.value
            ):
                raise HTTPException(
                    detail="Что не так сдадой рождения возможно не находится дипозоне 2025  или 1925",
                    status_code=400,
                )
        if filed_rating in data and data[filed_rating] is not None:
            if not await validet_star_rating(data, filed_rating):
                raise HTTPException(
                    detail="Что не так с оценкой возможно не находится в дипозоне 1 от 7",
                    status_code=402,
                )
        
        current_actpr= await self.get_actor_by_id(actor_id=actor_id)
        pat = current_actpr.patronymic
        lasname = current_actpr.lastname
        fistname = current_actpr.fistname
        if await self.actor_repo.get_duble_actor(
            actor_id, fistname=fistname, lastname=lasname, pat=pat
        ):
            raise HTTPException(detail="Такой актёр уже есть ", status_code=400)
        if image and image.filename:
                image_path = current_actpr.path_image
               
                delete_file(image_path)  
                fi = f"{lasname}_{fistname}"
                file_name = await uplodat_file_image_film_and_peplo(image,fi,type_model="peoples")
                clean_data["path_image"] = file_name
        update_actor = await self.actor_repo.update_actor(
            data=clean_data, actor_id=actor_id
        )
        if not update_actor:
            raise HTTPException(status_code=404, detail="Актёр не найден")
        return ActorResponse.from_orm(update_actor)

    async def get_actor_list(self, page: int = 1, limit: int = limit_people):
        actors = await self.actor_repo.get_actors(page=page, limit=limit)
        return ActorListResponse(actors=actors)

    async def get_actor_by_id(self, actor_id: UUID):
        actor = await self.actor_repo.get_actor_by_id(actor_id=actor_id)
        if not actor:
            raise HTTPException(status_code=404, detail="Актёр не найден")
        return Actor_FullResponse.from_orm(actor)
    async def get_count_actors(self):
        count_actors = await self.actor_repo.get_count_actors()
        return count_actors
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
        current_actpr= await self.get_actor_by_id(actor_id=actor_id)
        image_pat = current_actpr.path_image
        if image_pat:
            delete_file(image_pat)
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
