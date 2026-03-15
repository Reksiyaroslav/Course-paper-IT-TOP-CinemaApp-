from fastapi import APIRouter, HTTPException, Depends, Form,Request
from typing import Dict, List, Annotated
from fastapi.responses import RedirectResponse,HTMLResponse
from app.scheme.user.model_user import (
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
    UserRensponseAdmin,
    UserLogin,
    UserListResponse,
    
)
from app.scheme.film.model_film import FilmResponse,FilmlListBlockResponse
from uuid import UUID
from app.utils.depencines import UserService, get_user_service

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/")
async def create_user(reguest:Request,
    data: Annotated[UserCreateRequest, Form()],
    user_servers: UserService = Depends(get_user_service),
) -> HTMLResponse:
    user = await user_servers.create_user(data.dict())
    if not user:
        raise HTTPException(status_code=401, detail="not create user")
    url = reguest.url_for("log")
    return RedirectResponse(url)
@user_router.post("/login")
async def get_user_login_password(reguest:Request,data:Annotated[UserLogin,Form()],user_service:UserService = Depends(get_user_service)):
        user = await user_service.get_password_and_email(data.model_dump())
        reguest.session(user)
        return RedirectResponse("main_film")
@user_router.get("s/")
async def get_users(
    user_servers: UserService = Depends(get_user_service),
) -> UserListResponse:
    users = await user_servers.get_all_user()

    return UserListResponse(user_list=users)


@user_router.get("s/admin/")
async def get_admin_users(
    user_servers: UserService = Depends(get_user_service),
) -> UserListResponse:
    users = await user_servers.get_all_user()
    return UserListResponse(user_list=users)


@user_router.get("/profile/{user_id}")
async def get_user(
    user_id: UUID, user_services: UserService = Depends(get_user_service)
) -> UserResponse:
    user = await user_services.get_user_by_id(user_id)
    return UserResponse.from_orm(user)


@user_router.put("/{user_id}")
async def update_user(
    data: UserUpdateRequest,
    user_id: UUID,
    user_services: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await user_services.update_user(user_id, data.dict())
    return UserResponse.from_orm(user)


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
) -> Dict[str, str]:
    user = await user_service.delete_user(user_id)
    if user == None:
        return {"message": "Delete the db"}
    else:
        return {"message": "Что не удалось удалить"}


@user_router.post("/{user_id}/like_film/{film_id}")
async def add_likefilm(
    user_id: UUID, film_id: UUID, user_servers: UserService = Depends(get_user_service)
) -> UserResponse:
    user = await user_servers.add_film(user_id, film_id)
    if not user:
        raise HTTPException(detail="Not user the db", status_code=404)
    return UserResponse.from_orm(user)


@user_router.get("/likefilm/{user_id}")
async def get_list_likelilm(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
) -> FilmlListBlockResponse:
    films = await user_service.get_list_likefilm(user_id)
    if not films:
        raise HTTPException(
            detail="Не ту списко фильмовы у пользователя ", status_code=404
        )
    return FilmlListBlockResponse(films=films)
