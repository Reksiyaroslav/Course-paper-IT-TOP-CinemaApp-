from litestar import get ,Controller,post,put,delete
from app.repositories.ratingfilm_repositore import RatingFilmRepository
from app.model.model_ratingfilms import RatingFilmResponse,RatingFilmCreateRequest,RatingFilmUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from litestar.exceptions import HTTPException
from typing import Dict
from app.service.ratingfilms_service import RatingFilmService
from app.service.factory import get_service
class RatingFilmControlle(Controller):
    path ="/ratingfilm"
    tags = ["❌RatingFilm"]
    @post()
    async def create_ratingfilm(self,data:RatingFilmCreateRequest,async_session:AsyncSession)->RatingFilmResponse:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        ratingfilm = await ratingfilm_service.create_model(data.dict())
        if not ratingfilm:
            raise HTTPException("Not ratingfilm" ,status_code=404)
        return RatingFilmResponse.from_orm(ratingfilm)
    @post("/film/{film_id:uuid}/user/{user_id:uuid}")
    async def add_update_rating_film_and_user(self,film_id:UUID,user_id:UUID,rating:int,async_session:AsyncSession)->RatingFilmResponse:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        ratingfilm = await ratingfilm_service.add_update_film_and_user(film_id,user_id,rating)
        return RatingFilmResponse.from_orm(ratingfilm)
    @get()
    async def get_list_ratingfilm(self,async_session:AsyncSession)->list[RatingFilmResponse]:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        ratingfilms = await ratingfilm_service.get_models()
        return [RatingFilmResponse.from_orm(rating) for rating in ratingfilms ]
    @get("film/{film_id:uuid}")
    async def get_rating_film(self,film_id:UUID,async_session:AsyncSession)->list[RatingFilmResponse]:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        ratingfilms = await ratingfilm_service.get_list_film_rating(film_id)
        return [RatingFilmResponse.from_orm(rating) for rating in ratingfilms ]
    @get("user/{user_id:uuid}")
    async def get_rating_user(self,user_id:UUID,async_session:AsyncSession)->list[RatingFilmResponse]:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        ratingfilms = await ratingfilm_service.get_list_user_rating(user_id)
        return [RatingFilmResponse.from_orm(rating) for rating in ratingfilms ]
    @get("/{rating_film_id:uuid}")
    async def get_rating_id(self,rating_film_id:UUID,async_session:AsyncSession)->RatingFilmResponse:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        ratingfilm = await ratingfilm_service.get_model(rating_film_id)
        return RatingFilmResponse.from_orm(ratingfilm)
    @put("/{rating_film_id:uuid}")
    async def update_rating(self,rating_film_id:UUID,data:RatingFilmUpdateRequest,async_session:AsyncSession)->RatingFilmResponse:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        ratingfilm = await ratingfilm_service.update_model(rating_film_id,data.dict())
        if not ratingfilm:
            raise HTTPException("Not ratingfilm" ,status_code=404)
        return RatingFilmResponse.from_orm(ratingfilm)
    @delete("/{rating_film_id:uuid}",status_code=200)
    async def delete_ratingfilm(self,rating_film_id:UUID,async_session:AsyncSession)->dict:
        ratingfilm_service = get_service(RatingFilmService,RatingFilmRepository,async_session)
        rating = await ratingfilm_service.delete_model(rating_film_id)
        if not rating:
            raise HTTPException("Not ratingfilm" ,status_code=404)
        return {"detail": "RatingFilm deleted from db"}