from typing import Dict
from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import RedirectResponse
from uuid import UUID
from app.scheme.comment.model_coment import (
    ComentCreateRequest,
    ComentUpdateRequest,
)
from app.utils.depencines import ComentService, get_comment_service
from app.utils.router_help import get_curen_user
from app.handler.ui_api_route import teamlates


coment_router = APIRouter(prefix="/coment", tags=["Coment"])


@coment_router.post("/create_coment/{user_id}/{film_id}/")
async def create_comment(
    request: Request,
    film_id: UUID,
    user_id: UUID,
    description: str = Form(""),
    coment_sev: ComentService = Depends(get_comment_service),
    user=Depends(get_curen_user),
):
    try:
        data = ComentCreateRequest(description=description)
        await coment_sev.create_model(data.dict(), film_id, user_id)
        url = request.url_for("view_item", item_id=film_id, env_type_model="film")
        return RedirectResponse(url=url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "profile.html",
            context={
                "item_id": film_id,
                "env_type_model": "film",
                "user": user,
                "err": e.detail,
            },
        )


@coment_router.get("/s/")
async def get_comets(
    coment_sev: ComentService = Depends(get_comment_service),
):
    coments = await coment_sev.get_coments()
    return coments


@coment_router.get("/{coment_id}")
async def get_coment_coment_id(
    comnet_id: UUID, coment_sev: ComentService = Depends(get_comment_service)
):
    coment = await coment_sev.get_by_id_coment(comnet_id)
    return coment


@coment_router.post("/update/{coment_id}/{film_id}/")
@coment_router.put("/update/{coment_id}")
async def update_coment(
    request: Request,
    film_id: UUID,
    coment_id: UUID,
    description: str = Form(""),
    coment_sev: ComentService = Depends(get_comment_service),
    user=Depends(get_curen_user),
):
    try:
        data = ComentUpdateRequest(description=description)
        await coment_sev.update_coment(data=data.dict(), coment_id=coment_id)
        url = request.url_for("view_item", item_id=film_id, env_type_model="film")
        return RedirectResponse(url=url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "profile.html",
            context={
                "item_id": film_id,
                "env_type_model": "film",
                "user": user,
                "err": e.detail,
            },
        )


@coment_router.post("/update/like/{coment_id}/{film_id}/{user_id}/{type_rec}")
@coment_router.put("/update/like/{coment_id}/{film_id}")
async def update_coment_type_rec(
    request: Request,
    coment_id: UUID,
    film_id: UUID,
    type_rec: str,
    user_id: UUID,
    user=Depends(get_curen_user),
    coment_sev: ComentService = Depends(get_comment_service),
):
    try:
        await coment_sev.update_comet_like_unlike(
            coment_id=coment_id, user_id=user_id, type_rec=type_rec
        )
        url = request.url_for("view_item", item_id=film_id, env_type_model="film")
        return RedirectResponse(url=url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "profile.html",
            context={
                "item_id": film_id,
                "env_type_model": "film",
                "user": user,
                "err": e.detail,
            },
        )


@coment_router.post("/delete/{film_id}/{coment_id}/")
# @coment_router.delete("/delete/{film_id}/{coment_id}")
async def delete_coment(
    request: Request,
    film_id: UUID,
    coment_id: UUID,
    coment_sev: ComentService = Depends(get_comment_service),
):
    try:
        coment = await coment_sev.delete_coment(coment_id)
        url = request.url_for("view_item", item_id=film_id, env_type_model="film")
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "profiles.html",
            context={
                "request": request,
                "item_id": film_id,
                "env_type_model": "film",
                "err": e.detail,
            },
        )
