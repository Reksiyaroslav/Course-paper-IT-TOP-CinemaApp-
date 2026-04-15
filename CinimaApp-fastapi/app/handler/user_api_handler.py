from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse

from uuid import UUID
from app.utils.depencines import UserService, get_user_service
from app.scheme.user.model_user import (
    UserCreateRequest,
    UserUpdateRequest,
    UserLogin,
)
from app.handler.ui_api_route import teamlates
from app.utils.router_help import get_curen_user, clean_url_redirect

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/")
async def create_user(
    reguest: Request,
    username: str = Form(None),
    password: str = Form(None),
    email: str = Form(default=None),
    next: str = Form(""),
    user_servers: UserService = Depends(get_user_service),
):
    try:
        if (
            not username
            or not password
            or not username.strip()
            or not password.strip()
            or not email
        ):
            raise HTTPException(
                detail="Поля Имя пользователя и пароль не могу быть пустыми",
                status_code=400,
            )
        if len(username.strip()) < 5 or len(username.strip()) > 60:
            raise HTTPException(
                detail="Минемальная длина имени пользователя 5 и максимальная длина имени 60",
                status_code=400,
            )
        if len(password.strip()) < 8 or len(password.strip()) > 15:
            raise HTTPException(
                detail="Минемальная длина пароля  пользователя 8 и максимальная длина пароля 15",
                status_code=400,
            )
        data = UserCreateRequest(username=username, email=email, password=password)
        user = await user_servers.create_user(data.model_dump())
        url = reguest.url_for("main")
        return RedirectResponse(url)
    except HTTPException as e:
        url = clean_url_redirect(e.detail, next, "error_reg")
        return RedirectResponse(url=url)


@user_router.post("/login/")
async def get_user_login_email_password(
    reguest: Request,
    email_or_login: str = Form(None),
    password: str = Form(None),
    user_service: UserService = Depends(get_user_service),
    next: str = Form(""),
):
    try:
        clean_login_or_email = email_or_login.strip().lower()
        data = UserLogin(email=clean_login_or_email, password=password)
        user = await user_service.get_password_and_email(data.model_dump())
        reguest.session["user_id"] = str(user.user_id)
        reguest.session["email"] = user.email
        reguest.session["user_type"] = user.role_user
        url = reguest.url_for("main_item", type_model="film")
        return RedirectResponse(url=url)
    except HTTPException as e:
        url = clean_url_redirect(e.detail, next, "error_login")
        return RedirectResponse(url=url)


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


@user_router.post("/update_user/{user_id}/")
@user_router.put("/update_user/{user_id}/")
async def update_user(
    reguest: Request,
    user_id: UUID,
    username: str = Form(None),
    password: str = Form(None),
    user_services: UserService = Depends(get_user_service),
    user=Depends(get_curen_user),
):
    try:
        data = {}
        if not username or not password or not username.strip() or not password.strip():
            raise HTTPException(
                detail="Поля Имя пользователя и пароль не могу быть пустыми",
                status_code=400,
            )
        if len(username.strip()) < 5 or len(username.strip()) > 60:
            raise HTTPException(
                detail="Минемальная длина имени пользователя 5 и максимальная длина имени 60",
                status_code=400,
            )
        if len(password.strip()) < 8 or len(password.strip()) > 15:
            raise HTTPException(
                detail="Минемальная длина пароля  пользователя 8 и максимальная длина пароля 15",
                status_code=400,
            )
        data = UserUpdateRequest(username=username, password=password)
        await user_services.update_user(user_id, data.dict())
        url = reguest.url_for("view_item", item_id=user_id, env_type_model="user")
        return RedirectResponse(url)
    except HTTPException as e:
        return teamlates.TemplateResponse(
            "update_model.html",
            context={
                "request": reguest,
                "data": data,
                "err": e.detail,
                "type_model": "user",
                "model_id": user_id,
                "user": user,
            },
        )


@user_router.post("/delete/{user_id}/")
@user_router.delete("/delete/{user_id}/")
async def delete_user(
    reguest: Request,
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.delete_user(user_id)
        url = reguest.url_for("logout")
        return RedirectResponse(url)
    except HTTPException as e:
        url = reguest.url_for(
            "view_item", item_id=user_id, env_type_model="user", err=e.detail
        )
        return RedirectResponse(url)


@user_router.post("/{user_id}/like_film/{film_id}/")
async def add_likefilm(
    reguest: Request,
    user_id: UUID,
    film_id: UUID,
    user_servers: UserService = Depends(get_user_service),
):
    try:
        user = await user_servers.add_film(user_id, film_id)
        url = reguest.url_for("view_item", item_id=film_id, env_type_model="film")
        return RedirectResponse(url)
    except HTTPException as e:
        url = reguest.url_for(
            "view_item", item_id=film_id, env_type_model="film", err=e.detail
        )
        return RedirectResponse(url)


@user_router.post("/update_role_user/{user_admin_id}/{user_id}/")
async def update_user_role(
    request: Request,
    user_admin_id: UUID,
    user_id: UUID,
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


@user_router.get("/likefilm/{user_id}/")
async def get_list_likelilm(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    films = await user_service.get_list_likefilm(user_id)
    return films


@user_router.post("/likefilm/{user_id}/{film_id}/")
async def delete_likelilm(
    reguest: Request,
    user_id: UUID,
    film_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    try:
        films = await user_service.delete_like_film(user_id=user_id, film_id=film_id)
        url = reguest.url_for("view_item", item_id=film_id, env_type_model="film")
        return RedirectResponse(url)
    except HTTPException as e:

        url = reguest.url_for(
            "view_item", item_id=film_id, env_type_model="film", err=e.detail
        )
        return RedirectResponse(url)
