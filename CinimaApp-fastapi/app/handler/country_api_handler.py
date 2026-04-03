from fastapi import Request, APIRouter, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from uuid import UUID
from typing import Optional
from urllib.parse import urlencode
from app.scheme.country.model_country import (
    CountryCreateRequest,
    CountryUpdateRequest,
    CountryBaseResponse,
)
from app.utils.depencines import CountryService, get_country_service
from app.handler.ui_api_route import teamlates

country_router = APIRouter(prefix="/country", tags=["Country"])


@country_router.post(("/create_conntry"))
async def create_country(
    request: Request,
    name_country: str = Form(default=""),
    country_service: CountryService = Depends(get_country_service),
):
    try:
        countrys_relut = await country_service.get_countrys()
        countrys = countrys_relut.countrys
        data = {}
        len_name_country = len(name_country)
        if not name_country:
            raise HTTPException(detail="Не может быть ", status_code=400)
        if len_name_country < 3:
            raise HTTPException(detail="Минемальная длина 3", status_code=400)
        if len_name_country > 20:
            raise HTTPException(detail="Максимальное длина 20", status_code=400)
        data = CountryCreateRequest(country_name=name_country)
        country = await country_service.create_country(data=data.model_dump())
        url = request.url_for("show_type_film_country")
        return RedirectResponse(url=url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "type_film_and_countries.html",
            context={
                "request": request,
                "data": data,
                "type_model": "type_film",
                "type_action": "create",
                "err": e.detail,
                "countrys": countrys,
            },
        )


@country_router.post("/manager_country")
async def manager_country(
    request: Request,
    country_id: Optional[UUID] = Form(None),
    action_type: str = Form(default="list"),
    country_service: CountryService = Depends(get_country_service),
):
    base_url = request.url_for("show_type_film_country")
    if action_type == "create":
        reaquest = urlencode(
            {"type_action": "create", "type_model": "country", "item_id": country_id}
        )
        url = f"{base_url}?{reaquest}"
        return RedirectResponse(url)
    if action_type == "update":
        reaquest = urlencode(
            {"type_action": "update", "type_model": "country", "item_id": country_id}
        )
        url = f"{base_url}?{reaquest}"
        return RedirectResponse(url)
    if action_type == "delete":
        url = request.url_for("delete_country", country_id=country_id)
        return RedirectResponse(url)
    if not country_id:
        reaquest = urlencode({"messages": "Не нечего не оправили"})
        url = f"{base_url}?{reaquest}"
        return RedirectResponse(url, status_code=303)


@country_router.get(("s/"))
async def get_countrys(
    request: Request, country_service: CountryService = Depends(get_country_service)
):
    countrys = await country_service.get_countrys()

    return countrys


@country_router.get("/get_country/{country_id}")
async def get_country_by_id(
    request: Request,
    country_id: UUID,
    country_service: CountryService = Depends(get_country_service),
):
    country = await country_service.get_country_by_id(country_id=country_id)
    return country


@country_router.post("/update_country/{country_id}/")
async def update_country(
    request: Request,
    country_id: UUID,
    name_country: str = Form(default=""),
    country_service: CountryService = Depends(get_country_service),
):
    try:
        data = {}
        countrys_relut = await country_service.get_countrys()
        countrys = countrys_relut.countrys
        len_name_country = len(name_country)
        if not name_country:
            raise HTTPException(detail="Не может быть ", status_code=400)
        if len_name_country < 3:
            raise HTTPException(detail="Минемальная длина 3", status_code=400)
        if len_name_country > 20:
            raise HTTPException(detail="Максимальное длина 20", status_code=400)
        data = CountryUpdateRequest(country_name=name_country)
        country = await country_service.update_country(
            data=data.model_dump(), country_id=country_id
        )
        url = request.url_for("show_type_film_country")
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "type_film_and_countries.html",
            context={
                "request": request,
                "data": data,
                "type_model": "country",
                "type_action": "update",
                "err": e.detail,
                "item_id": country_id,
                "countrys": countrys,
            },
        )


@country_router.post("/delete_country/{country_id}/")
async def delete_country(
    request: Request,
    country_id: UUID,
    country_service: CountryService = Depends(get_country_service),
):
    try:
        country = await country_service.delete_country(country_id=country_id)
        url = request.url_for("show_type_film_country")
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "type_film_and_countries.html",
            context={
                "request": request,
                "type_model": "type_film",
                "type_action": "list",
                "err": e.detail,
            },
        )
