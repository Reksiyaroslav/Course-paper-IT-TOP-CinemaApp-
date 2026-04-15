from app.service.base_service import Base_Service
from uuid import UUID
from app.utils.comon import is_name_title
from fastapi.exceptions import HTTPException
from fastapi import status
from ..db.model.model_db import User, Role_User
from app.repositories.users_repositorie import UserRepository
from app.repositories.films_repositorie import FilmRepository
from app.enums.serach_fileld import SerachFiled
from app.enums.type_model import TypeModel

from app.utils.noramliz_text import normalize_data
from app.scheme.user.model_user import (
    UserResponse,
    UserListResponse,
    UserListAdminResponse,
    FilmBaseResponse,
    FilmBaseList,
)


class UserService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.user_repo: UserRepository = UserRepository(self.session)
        self.film_repo: FilmRepository = FilmRepository(self.session)

    async def create_user(self, data, name_title_value=None):
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.User.value)
        filed_username = SerachFiled.Name.value[4]
        if not await is_name_title(
            model=User,
            session=self.session,
            name_filed=filed_username,
            name_or_title_value=clean_data[filed_username],
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким именем уже существует",
            )
        new_user = await self.user_repo.create_user(clean_data)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании пользователя",
            )
        return {"messsage": "Вы прошли решгетрацию"}

    async def get_all_user(self):
        users = await self.user_repo.get_list_users()
        return UserListResponse(user_list=users)

    async def get_all_user_admin(self):
        users = await self.user_repo.get_list_users()

        return UserListAdminResponse(user_admin_list=users)

    async def get_user_by_id(self, user_id):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не найдено по запросу пользователь",
            )
        return UserResponse.from_orm(user)

    async def update_user(self, model_id, data):
        clean_data: dict = normalize_data(data=data, model_type=TypeModel.User.value)
        filed_username = SerachFiled.Name.value[4]
        if not await is_name_title(
            model=User,
            session=self.session,
            name_filed=filed_username,
            name_or_title_value=data[filed_username],
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким именем уже существует",
            )
        update_user = await self.user_repo.update_user(model_id, clean_data)
        if not update_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при обновлении пользователя",
            )
        return UserResponse.from_orm(update_user)

    async def delete_user(self, user_id):
        delete_user = await self.user_repo.delete_user(user_id)
        if not delete_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )
        return {"message": "Пользователь успешно удалён"}

    async def get_film_username(self, username: str):
        return await self.user_repo.get_name(username)

    async def add_film(self, user_id: UUID, film_id: UUID):
        try:
            film = await self.film_repo.get_film_by_id(film_id=film_id)
            user = await self.user_repo.add_licefilm(user_id, film)
            user = await self.get_user_by_id(user_id=user_id)
            return UserResponse.from_orm(user)
        except ValueError as e:
            raise HTTPException(detail=str(e), status_code=400)

    async def add_friend(self, user_id: UUID, friend_id: UUID):
        return await self.user_repo.add_frinde(user_id, friend_id)

    async def get_password_and_email(self, data: dict):
        user = await self.user_repo.get_username_password(data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )
        user_good = await self.get_user_by_id(user_id=user.user_id)
        return user_good

    async def get_list_likefilm(self, user_id: UUID):
        filmS = await self.user_repo.get_list_licefilm(user_id)
        return FilmBaseList(films=filmS)

    async def delete_like_film(self, user_id: UUID, film_id):
        film = await self.film_repo.get_film_by_id(film_id=film_id)
        user = await self.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(detail="Нет пользователя с id", status_code=404)
        if not film:
            raise HTTPException(detail="Нет такого фильма ", status_code=404)
        relult = await self.user_repo.delete_likefilm(film_id=film_id, user_id=user_id)
        if relult:
            return film
        else:
            raise HTTPException(status_code=400, detail="Удаления не прошло")

    async def user_update_role(
        self, user_id_admin: UUID, user_id_user: UUID, update_role_user: str
    ):
        user_admin = await self.get_user_by_id(user_id=user_id_admin)
        if not user_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь админа не найден",
            )
        if update_role_user not in Role_User:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Измение можно только admin author user",
            )
        if user_admin.role_user != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только администратор может менять роли",
            )
        if user_admin.role_user == "admin":
            update_user = await self.user_repo.set_user_role(
                user_id=user_id_user, role_user=update_role_user
            )
            if not update_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь которого обновляли не найден",
                )
            return UserResponse.from_orm(update_user)
        return UserResponse.from_orm(user_admin)
