from fastapi import Request, Form, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Optional
from uuid import UUID
from urllib.parse import urlencode
from app.handler.ui_api_route import teamlates
from app.scheme.film.type_film import (
    TypeFilmCreateRequest,
    TypeFilmResponse,
    TypeFilmUpdateRequest,
)
from app.utils.depencines import get_film_service, FilmService

type_film_router = APIRouter(prefix="/type_film", tags=["TypeFilm"])


@type_film_router.post(path="/create_type_film", response_model=None)
async def create_film_type(
    request: Request,
    type_film_name: str = Form(None),
    film_sevice: FilmService = Depends(get_film_service),
) -> HTMLResponse | RedirectResponse:
    try:
        data = {}
        type_relut = await film_sevice.get_types_film()
        types_film = type_relut.types_film
        len_type_name = len(type_film_name)
        if not type_film_name:
            raise HTTPException(detail="Не может быть ", status_code=400)
        if len_type_name < 5:
            raise HTTPException(detail="Минемальная длина 5", status_code=400)
        if len_type_name > 40:
            raise HTTPException(detail="Максимальное длина 40", status_code=400)
        data = TypeFilmCreateRequest(type_film_name=type_film_name)
        message = await film_sevice.create_type_film(data.model_dump())
        if isinstance(message, TypeFilmResponse):
            url = request.url_for("show_type_film_country")
            return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "type_film_and_countries.html",
            context={
                "request": request,
                "data": data,
                "type_model": "type_film",
                "type_action": "create",
                "types_film": types_film,
                "err": str(e),
            },
        )


@type_film_router.get("/manager_type_film/")
@type_film_router.post("/manager_type_film/")
async def manager_type_film(
    request: Request,
    type_film_id: Optional[UUID] = Form(None),
    action_type: str = Form(default="list"),
    film_sevice: FilmService = Depends(get_film_service),
):
    base_url = request.url_for("show_type_film_country")

    if action_type == "create":
        reaquest = urlencode(
            {
                "type_action": "create",
                "type_model": "type_film",
                "item_id": type_film_id,
            }
        )

        url = f"{base_url}?{reaquest}"
        return RedirectResponse(url)
    if action_type == "update":
        if not type_film_id:
            reaquest = urlencode({"err": "Не нечего не оправили"})
            url = f"{base_url}?{reaquest}"
            return RedirectResponse(url, status_code=303)
        reaquest = urlencode(
            {
                "type_action": "update",
                "type_model": "type_film",
                "item_id": type_film_id,
            }
        )
        url = f"{base_url}?{reaquest}"
        return RedirectResponse(url, status_code=303)
    if action_type == "delete":
        if not type_film_id:
            reaquest = urlencode({"err": "Не нечего не оправили"})
            url = f"{base_url}?{reaquest}"
            return RedirectResponse(url, status_code=303)
        url = request.url_for("delete_film_type", type_film_id=type_film_id)
        return RedirectResponse(url)


@type_film_router.get("s/")
async def get_films(
    film_service: FilmService = Depends(get_film_service),
):
    films = await film_service.get_types_film()
    return films


@type_film_router.get("/profile/{type_film_id}")
async def get_type_film_and_film_id(
    type_film_id: UUID, film_service: FilmService = Depends(get_film_service)
):
    film = await film_service.get_type_film_by_id(type_film_id=type_film_id)
    return film


@type_film_router.post("/update/{type_film_id}/")
async def update_type_film(
    type_film_id: UUID,
    request: Request,
    type_film_name: str = Form(None),
    film_service: FilmService = Depends(get_film_service),
):
    try:
        data = {}
        type_relut = await film_service.get_types_film()
        types_film = type_relut.types_film
        len_type_name = len(type_film_name)
        if not type_film_name:
            raise HTTPException(detail="Не может быть ", status_code=400)
        if len_type_name < 5:
            raise HTTPException(detail="Минемальная длина 5", status_code=400)
        if len_type_name > 40:
            raise HTTPException(detail="Максимальное длина 40", status_code=400)
        data = TypeFilmUpdateRequest(type_film_name=type_film_name)
        film = await film_service.update_type_film(
            type_film_id=type_film_id, data=data.model_dump()
        )
        url = request.url_for("show_type_film_country")
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "type_film_and_countries.html",
            context={
                "request": request,
                "type_model": "type_film",
                "data": data,
                "err": e.detail,
                "type_action": "update",
                "item_id": type_film_id,
                "types_film": types_film,
            },
        )


@type_film_router.post("/delete/{type_film_id}/")
async def delete_film_type(
    request: Request,
    type_film_id: UUID,
    film_service: FilmService = Depends(get_film_service),
):
    try:
        film = await film_service.delete_type_film(type_film_id)
        url = request.url_for("show_type_film_country")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("view_item", env_type_model="film", item_id=type_film_id)
        return RedirectResponse(url)
