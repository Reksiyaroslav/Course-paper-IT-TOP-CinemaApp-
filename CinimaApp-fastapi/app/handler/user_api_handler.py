from fastapi import APIRouter, HTTPException, Depends, Form, Request
from typing import Dict, Annotated
from fastapi.responses import RedirectResponse, HTMLResponse

from uuid import UUID
from app.utils.depencines import UserService, get_user_service
from app.scheme.user.model_user import (
    UserCreateRequest,
    UserUpdateRequest,
    UserLogin,
)
from app.handler.ui_api_route import teamlates

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/")
async def create_user(
    reguest: Request,
    data: Annotated[UserCreateRequest, Form()],
    user_servers: UserService = Depends(get_user_service),
) -> HTMLResponse:
    try:
        user = await user_servers.create_user(data.model_dump())
        url = reguest.url_for("log")
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "reg.html", context={"request": reguest, "data": data, "err": e.detail}
        )


@user_router.post("/login")
async def get_user_login_password(
    reguest: Request,
    email: str = Form(None),
    password: str = Form(None),
    user_service: UserService = Depends(get_user_service),
):
    try:
        data = UserLogin(email=email, password=password)
        user = await user_service.get_password_and_email(data.model_dump())
        reguest.session["user_id"] = str(user.user_id)
        reguest.session["email"] = user.email
        reguest.session["user_type"] = user.role_user
        url = reguest.url_for("main_item", type_model="film")
        return RedirectResponse(url=url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "log.html", context={"request": reguest, "data": data, "err": e.detail}
        )


@user_router.get("s/")
async def get_users(
    user_servers: UserService = Depends(get_user_service),
):
    users = await user_servers.get_all_user()

    return users


@user_router.get("s/admin/")
async def get_admin_users(
    user_servers: UserService = Depends(get_user_service),
):
    users = await user_servers.get_all_user_admin()
    return users


@user_router.get("/profile/{user_id}")
async def get_user(
    user_id: UUID, user_services: UserService = Depends(get_user_service)
):
    user = await user_services.get_user_by_id(user_id)
    return user


@user_router.post("/update_user/{user_id}")
@user_router.put("/{user_id}")
async def update_user(
    data: UserUpdateRequest,
    user_id: UUID,
    user_services: UserService = Depends(get_user_service),
):
    user = await user_services.update_user(user_id, data.dict())
    return user


@user_router.post("/delete/{user_id}")
@user_router.delete("/delete/{user_id}")
async def delete_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
) -> Dict[str, str]:
    user = await user_service.delete_user(user_id)
    return user


@user_router.post("/{user_id}/like_film/{film_id}")
async def add_likefilm(
    user_id: UUID, film_id: UUID, user_servers: UserService = Depends(get_user_service)
):
    user = await user_servers.add_film(user_id, film_id)
    return user


@user_router.post("/update_role_user/{user_admin_id}/")
async def update_user_role(
    request: Request,
    user_admin_id: UUID,
    user_id: UUID = Form(None),
    update_role_user: str = Form(""),
    user_servers: UserService = Depends(get_user_service),
):
    try:
        await user_servers.user_update_role(
            user_id_admin=user_admin_id,
            user_id_user=user_id,
            update_role_user=update_role_user,
        )
        return RedirectResponse(
            url=request.url_for("view_item", env_type_model="user", item_id=user_id),
            status_code=303,
        )

    except HTTPException as e:
        return RedirectResponse(
            url=request.url_for("update_form_role_user", err=e.detail), status_code=303
        )


@user_router.get("/likefilm/{user_id}")
async def get_list_likelilm(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    films = await user_service.get_list_likefilm(user_id)
    return films
