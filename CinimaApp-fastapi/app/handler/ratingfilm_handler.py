from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from uuid import UUID
from fastapi.exceptions import HTTPException
from starlette.templating import _TemplateResponse
from app.utils.depencines import RatingFilmService, get_rating_service
from app.scheme.rating.model_ratingfilms import (
    RatingFilmCreateRequest,
    RatingFilmUpdateRequest,
    RatingFilmResponse,
)
from app.handler.ui_api_route import teamlates

rating_router = APIRouter(prefix="/rating", tags=["Rating"])


@rating_router.post(path="/create_rating/{film_id}/{user_id}/")
async def create_rating(
    request: Request,
    film_id: UUID,
    user_id: UUID,
    rating: int = Form(0),
    rating_sev: RatingFilmService = Depends(get_rating_service),
):
    try:
        data = RatingFilmCreateRequest(rating=rating)
        rating = await rating_sev.create_ratingfilm(
            data=data.model_dump(), user_id=user_id, film_id=film_id
        )
        if isinstance(rating, RatingFilmResponse):
            url = request.url_for("view_item", env_type_model="film", item_id=film_id)
            return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "view_item.html",
            context={
                "request": request,
                "env_type_model": "film",
                "item_id": film_id,
                "err": e.detail,
            },
        )


@rating_router.get("s/")
async def list_api_rating(
    rating_sev: RatingFilmService = Depends(get_rating_service),
):
    ratings = await rating_sev.get_list_rating()
    return ratings


@rating_router.get("/{rating_id}")
async def get_rating_id(
    rating_id: UUID, rating_sev: RatingFilmService = Depends(get_rating_service)
):
    rating = await rating_sev.get_by_id_rating(rating_id)
    return rating


@rating_router.get("/admin/rating/")
async def get_list_admin_rating(
    rating_sev: RatingFilmService = Depends(get_rating_service),
):
    ratings = await rating_sev.get_list_rating()
    return ratings


@rating_router.get("/average/{film_id}")
async def average_rating_film(
    film_id: UUID, rating_sev: RatingFilmService = Depends(get_rating_service)
) -> dict[str, str]:
    average_rating = await rating_sev.average_rating_film(film_id)
    return {"message": f"Такой средний ратинг у фильма{average_rating}"}


@rating_router.post("/{rating_id}")
@rating_router.put("/{rating_id}")
async def update_rating(
    data: RatingFilmUpdateRequest,
    rating_id: UUID,
    rating_sev: RatingFilmService = Depends(get_rating_service),
):
    rating = await rating_sev.update_rating(data=data.dict(), rating_id=rating_id)
    return rating


@rating_router.post("/update/{film_id}/{user_id}/")
@rating_router.put("/update/{film_id}/{user_id}/")
async def update_rating_user_id(
    request: Request,
    user_id: UUID,
    film_id: UUID,
    rating: int = Form(0),
    rating_sev: RatingFilmService = Depends(get_rating_service),
):
    try:
        data = RatingFilmUpdateRequest(rating=rating)
        rating = await rating_sev.update_rating_user_id_and_film_id(
            data=data.model_dump(), user_id=user_id, film_id=film_id
        )
        if isinstance(rating, RatingFilmResponse):
            url = request.url_for("view_item", env_type_model="film", item_id=film_id)
            return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "view_item.html",
            context={
                "request": request,
                "env_type_model": "film",
                "item_id": film_id,
                "err": e.detail,
            },
        )


@rating_router.post("/delet/{rating_id}/{film_id}/")
async def delete_rating(
    request: Request,
    film_id: UUID,
    rating_id: UUID,
    rating_sev: RatingFilmService = Depends(get_rating_service),
):
    try:
        rating = await rating_sev.delete_rating(rating_id=rating_id, film_id=film_id)
        if isinstance(rating, dict):
            url = request.url_for("view_item", env_type_model="film", item_id=film_id)
            return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "view_item.html",
            context={
                "request": request,
                "env_type_model": "film",
                "item_id": film_id,
                "err": e.detail,
            },
        )
