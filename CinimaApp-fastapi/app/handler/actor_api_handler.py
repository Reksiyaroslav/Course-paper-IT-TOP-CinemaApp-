from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Optional
from app.scheme.actor.model_actor import (
    ActorCreateRequest,
    ActorUpdateRequest,
    ActorListResponse,
    datetime,
)
from app.utils.comon import Depends
from app.utils.router_help import parse_data_or_none
from app.utils.depencines import ActorService, get_actor_service
from uuid import UUID

actor_router = APIRouter(prefix="/actor", tags=["Actor"])


@actor_router.post(path="/create_actor", response_model=None)
async def create_actor(
    request: Request,
    fistname: str = Form(None),
    lastname: str = Form(None),
    birth_date: str = Form(None),
    patronymic: str = Form(None),
    star: int = Form(1),
    country_id: UUID = Form(default=None),
    actor_service: ActorService = Depends(get_actor_service),
) -> RedirectResponse | HTMLResponse:
    try:
        len_fistname = len(fistname)
        len_lastname = len(lastname)
        len_patronymic = len(patronymic)
        parse_date = parse_data_or_none(date_str=birth_date, field_name="birth_date")
        if not fistname:
            raise HTTPException(detail="Не может быть пустым Имя", status_code=400)
        if not lastname:
            raise HTTPException(
                detail="Не может быть пустым  Фамилия ", status_code=400
            )
        if not patronymic:
            raise HTTPException(
                detail="Не может быть пустым  Отчества ", status_code=400
            )
        if not parse_date:
            raise HTTPException(
                detail="Не может быть пустым  Дата рождения ", status_code=400
            )
        if len_patronymic < 3 or len_lastname < 3 or len_fistname < 3:
            raise HTTPException(detail="Минимальная длина 3", status_code=400)
        if len_patronymic > 50 or len_lastname > 50 or len_fistname > 50:
            raise HTTPException(detail="Максимальная длина 50", status_code=400)
        data = ActorCreateRequest(
            fistname=fistname,
            lastname=lastname,
            birth_date=parse_date,
            patronymic=patronymic,
            star=star,
        )

        actor = await actor_service.create_actor(data.model_dump())
        if country_id:
            await actor_service.add_country(
                actor_id=actor.actor_id, country_id=country_id
            )
        url = request.url_for("main_item", type_model="actor")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("create_model", type_model="actor", err=e.detail)
        return RedirectResponse(url)


@actor_router.get("s/")
async def get_actors(
    actor_service: ActorService = Depends(get_actor_service),
) -> ActorListResponse:
    actors = await actor_service.get_actor_list()
    return actors


@actor_router.get("/profile/{actor_id}")
async def get_actor_actor_id(
    actor_id: UUID, actor_service: ActorService = Depends(get_actor_service)
):
    actor = await actor_service.get_actor_by_id(actor_id)
    return actor


@actor_router.get("/name_actors/{fistname_latname_pat}")
async def get_name_actors(
    fistname_latname_pat: str, actor_service: ActorService = Depends(get_actor_service)
) -> ActorListResponse:
    actors = await actor_service.get_serahc_name_list(fistname_latname_pat)
    return actors


@actor_router.post("/update/{actor_id}")
async def update_actor(
    reguest: Request,
    actor_id: UUID,
    fistname: str = Form(None),
    lastname: str = Form(None),
    birth_date: datetime.date = Form(None),
    patronymic: str = Form(None),
    star: int = Form(1),
    country_id: UUID = Form(default=None),
    actor_service: ActorService = Depends(get_actor_service),
):
    try:
        len_fistname = len(fistname)
        len_lastname = len(lastname)
        len_patronymic = len(patronymic)
        if not fistname or not lastname or not patronymic:
            raise HTTPException(
                detail="Не может быть пустым имя фамилия отчества и дата рождения",
                status_code=400,
            )
        if len_patronymic < 3 or len_lastname < 3 or len_fistname < 3:
            raise HTTPException(detail="Минимальная длина 3", status_code=400)
        if len_patronymic > 50 or len_lastname > 50 or len_fistname > 50:
            raise HTTPException(detail="Максимальная длина 50", status_code=400)
        data = ActorUpdateRequest(
            fistname=fistname,
            lastname=lastname,
            patronymic=patronymic,
            birth_date=birth_date,
            star=star,
            country_id=country_id,
        )
        actor = await actor_service.update_actor(actor_id=actor_id, data=data.dict())
        if country_id:
            await actor_service.set_country(actor_id=actor_id, country_id=country_id)
        url = reguest.url_for("view_item", env_type_model="actor", item_id=actor_id)
        return RedirectResponse(url)
    except HTTPException as e:
        url = reguest.url_for(
            "update_model", item_id=actor_id, env_type_model="actor", err=e.detail
        )
        return RedirectResponse(url)


@actor_router.post("/delete/{actor_id}/")
@actor_router.delete("/delete/{actor_id}/")
async def delete_actor(
    request: Request,
    actor_id: UUID,
    actor_service: ActorService = Depends(get_actor_service),
):
    try:
        actor = await actor_service.delete_actor(actor_id)
        url = request.url_for("main_item", type_model="actor")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("view_item", env_type_model="actor", item_id=actor_id)
        return RedirectResponse(url)
