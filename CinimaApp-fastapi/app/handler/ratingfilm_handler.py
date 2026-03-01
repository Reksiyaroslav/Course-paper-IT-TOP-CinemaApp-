from app.scheme.model_ratingfilms import (
    RatingFilmCreateRequest,
    RatingFilmResponse,
    RatingFilmUpdateRequest,
    RatingFilmResponseAdmin,
)
from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from fastapi.exceptions import HTTPException
from app.utils.depencines import RatingFilmService, get_rating_service

rating_router = APIRouter(prefix="/rating", tags=["Rating"])


@rating_router.post("/create_rating/{fillm_id}/{user_id}/")
async def create_rating(
    data: RatingFilmCreateRequest,
    film_id: UUID,
    user_id: UUID,
    rating_sev: RatingFilmService = Depends(get_rating_service),
) -> RatingFilmResponse | dict:
    rating = await rating_sev.create_ratingfilm(data.dict(), user_id, film_id)
    if isinstance(rating, dict):
        return rating
    else:
        return RatingFilmResponse.from_orm(rating)


@rating_router.get("s/")
async def list_api_rating(
    rating_sev: RatingFilmService = Depends(get_rating_service),
) -> List[RatingFilmResponse]:
    ratings = await rating_sev.get_list_rating()
    return [RatingFilmResponse.from_orm(rating) for rating in ratings]


@rating_router.get("/{rating_id}")
async def get_rating_id(
    rating_id: UUID, rating_sev: RatingFilmService = Depends(get_rating_service)
) -> RatingFilmResponse:
    rating = await rating_sev.get_by_id_rating(rating_id)
    return RatingFilmResponse.from_orm(rating)


@rating_router.get("/admin/rating/")
async def get_list_admin_rating(
    rating_sev: RatingFilmService = Depends(get_rating_service),
) -> List[RatingFilmResponseAdmin]:
    ratings = await rating_sev.get_list_rating()
    return [RatingFilmResponseAdmin.from_orm(rating) for rating in ratings]


@rating_router.get("/average/{film_id}")
async def average_rating_film(
    film_id: UUID, rating_sev: RatingFilmService = Depends(get_rating_service)
) -> dict[str, str]:
    average_rating = await rating_sev.average_rating_film(film_id)
    return {"message": f"Такой средний ратинг у фильма{average_rating}"}


@rating_router.put("/{rating_id}")
async def update_rating(
    data: RatingFilmUpdateRequest,
    rating_id: UUID,
    rating_sev: RatingFilmService = Depends(get_rating_service),
) -> RatingFilmResponse:
    rating = await rating_sev.update_rating(data=data.dict(), rating_id=rating_id)
    if not rating:
        raise HTTPException(detail="Нет такого ратинга", status_code=404)
    return RatingFilmResponse.from_orm(rating)


@rating_router.put("/update/")
async def update_rating_user_id(
    data: RatingFilmUpdateRequest,
    user_id: UUID,
    film_id: UUID,
    rating_sev: RatingFilmService = Depends(get_rating_service),
) -> RatingFilmResponse:
    rating = await rating_sev.update_rating_user_id_and_film_id(
        data=data.dict(), user_id=user_id, film_id=film_id
    )
    if not rating:
        raise HTTPException(detail="Not rating db", status_code=402)
    return RatingFilmResponse.from_orm(rating)


@rating_router.delete("/delet/{rating_id}")
async def delete_rating(
    rating_id: UUID, rating_sev: RatingFilmService = Depends(get_rating_service)
) -> dict[str, str]:
    rating = await rating_sev.delete_rating(rating_id)
    return {"message": "Удалание этого ретинга"}
