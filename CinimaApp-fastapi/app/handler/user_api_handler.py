from fastapi import APIRouter, HTTPException
from typing import Dict, List
from app.scheme.model_user import UserCreateRequest, UserResponse, UserUpdateRequest
from app.service.user_service import UserService
from app.repositories.users_repositorie import UserRepository
from app.scheme.model_film import FilmResponse
from app.service.factory import get_service
from uuid import UUID

user_router = APIRouter(prefix="/user", tags=["User"])
from app.utils.comon import SessionDep


@user_router.post("/")
async def create_user(
    data: UserCreateRequest, async_session: SessionDep
) -> UserResponse:
    users_servers = await get_service(UserService, UserRepository, async_session)
    user = await users_servers.create_model(data.dict())
    if not user:
        raise HTTPException(status_code=401, detail="not create user")
    return UserResponse.model_validate(user)


@user_router.get("s/")
async def get_users(
    async_session: SessionDep,
) -> List[UserResponse]:
    users_servers = await get_service(UserService, UserRepository, async_session)
    users = await users_servers.get_models()
    return [UserResponse.from_orm(user) for user in users]


@user_router.get("/{user_id}")
async def get_user(user_id: UUID, async_session: SessionDep) -> UserResponse:
    users_servers = await get_service(UserService, UserRepository, async_session)
    user = await users_servers.get_model(user_id)
    return UserResponse.from_orm(user)


@user_router.put("/{user_id}")
async def update_user(
    data: UserUpdateRequest,
    user_id: UUID,
    async_session: SessionDep,
) -> UserResponse:
    users_servers = await get_service(UserService, UserRepository, async_session)
    user = await users_servers.update_model(user_id, data.dict())
    return UserResponse.from_orm(user)


@user_router.delete("/{user_id}")
async def delete_user(user_id: UUID, async_session: SessionDep) -> Dict[str, str]:
    users_servers = await get_service(UserService, UserRepository, async_session)
    user = await users_servers.delete_model(user_id)
    if not user:
        raise HTTPException(detail="Not user the db", status_code=404)
    return {"message": "Delete the db"}


@user_router.post("/{user_id}/like_film/{film_id}")
async def add_likefilm(
    user_id: UUID, film_id: UUID, async_session: SessionDep
) -> UserResponse:
    users_servers = await get_service(UserService, UserRepository, async_session)
    user = await users_servers.add_film(user_id, film_id)
    if not user:
        raise HTTPException(detail="Not user the db", status_code=404)
    return UserResponse.from_orm(user)


@user_router.get("/likefilm/{user_id}")
async def get_list_likelilm(
    user_id: UUID, async_session: SessionDep
) -> List[FilmResponse]:
    users_servers = await get_service(UserService, UserRepository, async_session)
    films = await users_servers.get_list_likefilm(user_id)
    if not films:
        raise HTTPException(
            detail="Не ту списко фильмовы у пользователя ", status_code=404
        )
    return [FilmResponse.from_orm(film) for film in films]
