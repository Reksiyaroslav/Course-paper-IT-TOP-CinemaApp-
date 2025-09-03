from app.scheme.model_ratingfilms import (
    RatingFilmCreateRequest,
    RatingFilmResponse,
    RatingFilmUpdateRequest,
)
from app.repositories.ratingfilm_repositore import RatingFilmRepository
from app.service.ratingfilms_service import RatingFilmService
from app.utils.comon import SessionDep
from app.service.factory import get_service
from fastapi import APIRouter
from typing import List
from uuid import UUID
from fastapi.exceptions import HTTPException

rating_router = APIRouter(prefix="/rating", tags=["Rating"])


@rating_router.post("/create_rating/{fillm_id}/{user_id}/")
async def create_rating(
    data: RatingFilmCreateRequest,
    async_session: SessionDep,
    film_id: UUID,
    user_id: UUID,
) -> RatingFilmResponse:
    rating_sev = await get_service(
        RatingFilmService, RatingFilmRepository, async_session
    )
    rating = await rating_sev.create_ratingfilm(data.dict(), user_id, film_id)
    return RatingFilmResponse.from_orm(rating)


@rating_router.get("s/")
async def list_api_rating(async_session: SessionDep) -> List[RatingFilmResponse]:
    rating_sev = await get_service(
        RatingFilmService, RatingFilmRepository, async_session
    )
    ratings = await rating_sev.get_models()
    return [RatingFilmResponse.from_orm(rating) for rating in ratings]


@rating_router.get("/{rating_id}")
async def get_rating_id(
    rating_id: UUID, async_session: SessionDep
) -> RatingFilmResponse:
    rating_sev = await get_service(
        RatingFilmService, RatingFilmRepository, async_session=async_session
    )
    rating = await rating_sev.get_model(rating_id)
    return RatingFilmResponse.from_orm(rating)


@rating_router.get("/average/{film_id}")
async def average_rating_film(
    film_id: UUID, async_session: SessionDep
) -> dict[str, str]:
    rating_sev = await get_service(
        RatingFilmService, RatingFilmRepository, async_session
    )
    average_rating = await rating_sev.average_rating_film(film_id)
    return {"message": f"Такой средний ратинг у фильма{average_rating}"}


@rating_router.put("/{rating_id}")
async def update_rating(
    data: RatingFilmUpdateRequest, async_session: SessionDep, rating_id: UUID
) -> RatingFilmResponse:
    rating_sev = await get_service(
        RatingFilmService, RatingFilmRepository, async_session
    )
    rating = await rating_sev.update_model(data.dict(), rating_id)
    if not rating:
        raise HTTPException(detail="Нету такого ратинга", status_code=404)
    return RatingFilmResponse.from_orm(rating)


@rating_router.delete("/delet/{rating_id}")
async def delete_rating(rating_id: UUID, async_session: SessionDep) -> dict[str, str]:
    rating_sev = await get_service(
        RatingFilmService, RatingFilmRepository, async_session
    )
    rating = await rating_sev.delete_model(rating_id)
    return {"message": f"Удалание этого ретинга"}
