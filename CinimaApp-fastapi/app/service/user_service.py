from app.service.base_service import Base_Service
from uuid import UUID
from app.utils.comon import is_name_title
from fastapi.exceptions import HTTPException
from app.list.list_searhc import list_serach_name_title


class UserService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)

    async def create_model(self, data, name_title_value=None):
        if not await is_name_title(
            model=self.repo.model,
            session=self.repo.session,
            name_filed=list_serach_name_title[4],
            name_or_title_value=data[list_serach_name_title[4]],
        ):
            raise HTTPException(
                status_code=409, detail="Пользователь с таким именем уже существует"
            )
        return await super().create_model(data, name_title_value)

    async def update_model(self, model_id, data):
        if not await is_name_title(
            model=self.repo.model,
            session=self.repo.session,
            name_filed=list_serach_name_title[4],
            name_or_title_value=data[list_serach_name_title[4]],
        ):
            raise HTTPException(
                status_code=409, detail="Пользователь с таким именем уже существует"
            )
        return await super().update_model(model_id, data)

    async def get_film_username(self, username: str):
        return await self.repo.get_name(username)

    async def add_film(self, user_id: UUID, film_id: UUID):
        return await self.repo.add_licefilm(user_id, film_id)

    async def add_friend(self, user_id: UUID, friend_id: UUID):
        return await self.repo.add_frinde(user_id, friend_id)

    async def get_password_and_username(self, username: str, password: str):
        return await self.repo.get_username_password(username, password)

    async def get_list_likefilm(self, user_id: UUID):
        return await self.repo.get_list_licefilm(user_id)
