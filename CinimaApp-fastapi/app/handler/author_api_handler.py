from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from datetime import date
from app.scheme.author.model_author import (
    AuthorUpdateRequest,
    AuthorCreateRequest,
    AuthorlListResponse,
)
from app.utils.comon import Depends
from app.utils.depencines import (
    AuthorService,
    get_author_service,
    CountryService,
    get_country_service,
)
from uuid import UUID
from app.handler.ui_api_route import teamlates

author_router = APIRouter(prefix="/author", tags=["Author"])


@author_router.post("/")
async def create_author(
    request: Request,
    fistname=Form(None),
    lastname=Form(None),
    bio: str = Form(None),
    birth_date: date = Form(None),
    patronymic: str = Form(None),
    country_id: UUID = Form(default=None),
    author_service: AuthorService = Depends(get_author_service),
    country_service: CountryService = Depends(get_country_service),
):
    try:
        len_fistname = len(fistname)
        len_lastname = len(lastname)
        len_patronymic = len(patronymic)
        if not fistname or not lastname or not patronymic or birth_date:
            raise HTTPException(
                detail="Не может быть пустым имя фамилия отчества", status_code=400
            )
        if len_patronymic < 3 or len_lastname < 3 or len_fistname < 3:
            raise HTTPException(detail="Минимальная длина 3", status_code=400)
        if len_patronymic > 50 or len_lastname > 50 or len_fistname > 50:
            raise HTTPException(detail="Максимальная длина 50", status_code=400)
        country_relut = await country_service.get_countrys()
        countrys = country_relut.countrys
        data = AuthorCreateRequest(
            fistname=fistname,
            lastname=lastname,
            bio=bio,
            birth_date=birth_date,
            patronymic=patronymic,
        )
        author = await author_service.create_author(data.dict())
        if country_id:
            await author_service.add_country(
                author_id=author.author_id, country_id=country_id
            )
        url = request.url_for("main_item", type_model="author")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("create_model", type_model="author", err=e.detail)
        return RedirectResponse(url)


@author_router.get("s/")
async def get_authors(
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorlListResponse:
    authors = await author_service.get_authors()
    return authors


@author_router.get("/profile/{actor_id}")
async def get_author_id(
    author_id: UUID, author_service: AuthorService = Depends(get_author_service)
):
    author = await author_service.get_author_by_id(author_id)
    if not author:
        raise HTTPException(detail="Не найдено такой актёр", status_code=404)
    return author


@author_router.get("/name_authors/{fistname_latname_pat}")
async def get_name_authors(
    fistname_latname_pat: str,
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorlListResponse:
    authors = await author_service.get_fistname_lastname_pat_list(fistname_latname_pat)
    return authors


@author_router.post("/update/{author_id}")
async def update_author(
    request: Request,
    author_id: UUID,
    fistname=Form(None),
    lastname=Form(None),
    bio: str = Form(None),
    birth_date: date = Form(None),
    patronymic: str = Form(None),
    country_id: UUID = Form(default=None),
    author_service: AuthorService = Depends(get_author_service),
):
    try:
        len_fistname = len(fistname)
        len_lastname = len(lastname)
        len_patronymic = len(patronymic)
        if not fistname or not lastname or not patronymic or not birth_date:
            raise HTTPException(
                detail="Не может быть пустыми имя фамилия отчества дата рождения",
                status_code=400,
            )
        if len_patronymic < 3 or len_lastname < 3 or len_fistname < 3:
            raise HTTPException(detail="Минимальная длина 3", status_code=400)
        if len_patronymic > 50 or len_lastname > 50 or len_fistname > 50:
            raise HTTPException(detail="Максимальная длина 50", status_code=400)
        data = AuthorUpdateRequest(
            fistname=fistname,
            lastname=lastname,
            bio=bio,
            birth_date=birth_date,
            patronymic=patronymic,
        )
        author = await author_service.update_author(author_id, data.dict())
        if country_id:
            await author_service.add_country(author_id=author_id, country_id=country_id)
        url = request.url_for("view_item", env_type_model="author", item_id=author_id)
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for(
            "update_model", item_id=author_id, env_type_model="author", err=e.detail
        )
        return RedirectResponse(url)


@author_router.post("/delete/{author_id}")
@author_router.delete("/delete/{author_id}")
async def delete_author(
    request: Request,
    author_id: UUID,
    author_service: AuthorService = Depends(get_author_service),
):
    try:
        author = await author_service.delete_author(author_id)
        url = request.url_for("main_item", type_model="author")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("view_item", env_type_model="author", item_id=author_id)
        return RedirectResponse(url)
