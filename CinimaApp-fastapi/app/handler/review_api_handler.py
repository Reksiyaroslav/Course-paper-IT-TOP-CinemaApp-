from fastapi import Depends, Form, Request, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from uuid import UUID
from app.handler.ui_api_route import teamlates
from app.utils.depencines import ReviewSevice, get_review_service
from app.scheme.review.model_review import CreateReview, UpdateReview

review_router = APIRouter(prefix="/review", tags=["Review"])


@review_router.post("/create_review/{film_id}/{user_id}/")
async def create_review(
    request: Request,
    film_id: UUID,
    user_id: UUID,
    description: str = Form(default=None),
    rating_histrory_str: str = Form(default=None),
    rating_atmosphere_str: str = Form(default=None),
    rating_musing_str: str = Form(default=None),
    rating_persons_str: str = Form(default=None),
    is_reviewrs: bool = Form(default=False),
    review_service: ReviewSevice = Depends(get_review_service),
):
    try:
        if not description.strip() or not description:
            raise HTTPException(status_code=400, detail="Нету описание у рецензий")
        if len(description) < 50:
            raise HTTPException(
                status_code=400, detail="Минемальная длина опсиание у реценизий 50"
            )
        if len(description) > 500:
            raise HTTPException(
                status_code=400, detail="Максимальная длина опсиание у реценизий 500"
            )
        rating_histrory, rating_atmosphere, rating_musing, rating_persons = (
            int(rating_histrory_str),
            int(rating_atmosphere_str),
            int(rating_musing_str),
            int(rating_persons_str),
        )
        data = CreateReview(
            description=description.strip(),
            rating_histrory=rating_histrory,
            rating_atmosphere=rating_atmosphere,
            rating_musing=rating_musing,
            rating_persons=rating_persons,
            is_reviewer=is_reviewrs,
        )
        review = await review_service.create_review(
            data=data.model_dump(), user_id=user_id, film_id=film_id
        )
        url = request.url_for(
            "view_item", env_type_model="film", item_id=film_id, type_view="review"
        )
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for(
            "view_item",
            env_type_model="film",
            item_id=film_id,
            err=e.detail,
            type_view="review",
        )
        return RedirectResponse(url)


@review_router.get("/list_review/")
async def get_list_review(review_service: ReviewSevice = Depends(get_review_service)):
    revewis = await review_service.get_list_reviews()
    return revewis


@review_router.get("/list_review/{review_id}/")
async def get_review_by_id(
    review_id: UUID, review_service: ReviewSevice = Depends(get_review_service)
):
    revewis = await review_service.get_by_id_review(review_id)
    return revewis


@review_router.post("/update_reviwe/{review_id}/{film_id}/")
async def update_review(
    request: Request,
    film_id: UUID,
    review_id: UUID,
    description: str = Form(default=None),
    rating_histrory_str: str = Form(default=None),
    rating_atmosphere_str: str = Form(default=None),
    rating_musing_str: str = Form(default=None),
    rating_persons_str: str = Form(default=None),
    is_reviewrs: bool = Form(default=False),
    review_service: ReviewSevice = Depends(get_review_service),
):
    try:
        if not description.strip() or not description:
            raise HTTPException(status_code=400, detail="Нету описание у рецензий")
        if len(description) < 100:
            raise HTTPException(
                status_code=400, detail="Минемальная длина опсиание у реценизий 100"
            )
        if len(description) > 500:
            raise HTTPException(
                status_code=400, detail="Максимальная длина опсиание у реценизий 500"
            )
        rating_histrory, rating_atmosphere, rating_musing, rating_persons = (
            int(rating_histrory_str),
            int(rating_atmosphere_str),
            int(rating_musing_str),
            int(rating_persons_str),
        )
        data = CreateReview(
            description=description,
            rating_histrory=rating_histrory,
            rating_atmosphere=rating_atmosphere,
            rating_musing=rating_musing,
            rating_persons=rating_persons,
            is_reviewer=is_reviewrs,
        )
        review = await review_service.update_review(
            data=data.model_dump(), review_id=review_id, film_id=film_id
        )
        url = request.url_for(
            "view_item", env_type_model="film", item_id=film_id, type_view="review"
        )
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for(
            "view_item",
            env_type_model="film",
            item_id=film_id,
            err=e.detail,
            type_view="review",
        )
        return RedirectResponse(url)


@review_router.post("/delete_review/{review_id}/{film_id}/")
async def delete_review(
    request: Request,
    film_id: UUID,
    review_id: UUID,
    review_service: ReviewSevice = Depends(get_review_service),
):
    try:
        sus = await review_service.delete_review(review_id=review_id, film_id=film_id)
        url = request.url_for("view_item", env_type_model="film", item_id=film_id, type_view="review")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for(
            "view_item",
            env_type_model="film",
            item_id=film_id,
            err=e.detail,
            type_view="review",
        )
        return RedirectResponse(url)
