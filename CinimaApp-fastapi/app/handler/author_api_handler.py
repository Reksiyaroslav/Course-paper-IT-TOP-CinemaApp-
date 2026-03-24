from typing import Dict, Annotated
from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from datetime import date
from app.scheme.author.model_author import (
    AuthorResponse,
    AuthorUpdateRequest,
    AuthorCreateRequest,
    AuthorlListResponse,
)
from app.utils.comon import Depends
from app.utils.depencines import AuthorService, get_author_service
from uuid import UUID
from app.handler.ui_api_route import teamlates

author_router = APIRouter(prefix="/author", tags=["Author"])


@author_router.post("/")
async def create_author(
    request: Request,
    data: Annotated[AuthorCreateRequest, Form()],
    author_service: AuthorService = Depends(get_author_service),
):
    try:
        author = await author_service.create_author(data.dict())
        url = request.url_for("main_author")
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "create_model.html",
            context={
                "request": request,
                "data": data,
                "err": e.detail,
                "type_model": "author",
            },
        )


@author_router.get("s/")
async def get_authors(
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorlListResponse:
    authors = await author_service.get_authors()
    return authors


@author_router.get("/profile/{actor_id}")
async def get_author_id(
    author_id: UUID, author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
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
    author_service: AuthorService = Depends(get_author_service),
):
    try:
        data = AuthorUpdateRequest(
            fistname=fistname,
            lastname=lastname,
            bio=bio,
            birth_date=birth_date,
            patronymic=patronymic,
        )
        author = await author_service.update_author(author_id, data.dict())
        url = request.url_for("view_item", env_type_model="author", item_id=author_id)
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "update_model.html",
            context={
                "request": request,
                "data": data,
                "err": e.detail,
                "type_model": "author",
                "model_id": author_id,
            },
        )


@author_router.post("/delete/{author_id}")
@author_router.delete("/delete/{author_id}")
async def delete_author(
    request: Request,
    author_id: UUID,
    author_service: AuthorService = Depends(get_author_service),
):
    try:
        author = await author_service.delete_author(author_id)
        url = request.url_for("main_author")
        return RedirectResponse(url)
    except HTTPException as e:
        url = request.url_for("view_item", env_type_model="author", item_id=author_id)
        return RedirectResponse(url)
