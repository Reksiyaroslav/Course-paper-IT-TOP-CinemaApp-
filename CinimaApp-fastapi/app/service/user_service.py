from app.service.base_service import Base_Service
from uuid import UUID
from app.utils.comon import is_name_title
from fastapi.exceptions import HTTPException
from app.list.list_searhc import list_serach_name_title
from ..db.model.model_db import User
from app.repositories.users_repositorie import UserRepository


class UserService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.user_repo = UserRepository(self.session)

    async def create_user(self, data, name_title_value=None):
        if not await is_name_title(
            model=User,
            session=self.session,
            name_filed=list_serach_name_title[4],
            name_or_title_value=data[list_serach_name_title[4]],
        ):
            raise HTTPException(
                status_code=409, detail="Пользователь с таким именем уже существует"
            )
        return await self.user_repo.create_user(data)

    async def get_all_user(self):
        return await self.user_repo.get_list_users()

    async def get_user_by_id(self, user_id):
        return await self.user_repo.get_user_by_id(user_id)

    async def update_user(self, model_id, data):
        if not await is_name_title(
            model=User,
            session=self.session,
            name_filed=list_serach_name_title[4],
            name_or_title_value=data[list_serach_name_title[4]],
        ):
            raise HTTPException(
                status_code=409, detail="Пользователь с таким именем уже существует"
            )
        return await self.user_repo.update_user(model_id, data)

    async def delete_user(self, user_id):
        return await self.user_repo.delete_user(user_id)

    async def get_film_username(self, username: str):
        return await self.user_repo.get_name(username)

    async def add_film(self, user_id: UUID, film_id: UUID):
        return await self.user_repo.add_licefilm(user_id, film_id)

    async def add_friend(self, user_id: UUID, friend_id: UUID):
        return await self.user_repo.add_frinde(user_id, friend_id)

    async def get_password_and_username(self, username: str, password: str):
        return await self.user_repo.get_username_password(username, password)

    async def get_list_likefilm(self, user_id: UUID):
        return await self.user_repo.get_list_licefilm(user_id)
