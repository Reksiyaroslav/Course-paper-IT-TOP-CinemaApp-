from app.service.base_service import Base_Service
from uuid import UUID
from fastapi.exceptions import HTTPException
from app.utils.comon import is_fistname_lastname, validate_is_data_range
from app.list.list_searhc import list_serach_date


class AuthorService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)

    async def create_model(self, data, name_title_value=None):
        if await validate_is_data_range(data[list_serach_date[1]], "author"):
            if not await is_fistname_lastname(self.repo.model, self.repo.session, data):
                raise HTTPException(detail="Такой автор уже есть ", status_code=400)
            return await super().create_model(data, name_title_value)
        raise HTTPException(
            detail="Что не так сдадой рождения возможно не находится дипозоне 2025  или 1945",
            status_code=404,
        )

    async def update_model(self, model_id, data):
        if await validate_is_data_range(data[list_serach_date[1]], "author"):
            if not await is_fistname_lastname(self.repo.model, self.repo.session, data):
                raise HTTPException(detail="Такой автор уже есть ", status_code=400)
            return await super().update_model(model_id, data)
        raise HTTPException(
            detail="Что не так сдадой рождения возможно не находится дипозоне 2025  или 1945",
            status_code=404,
        )

    async def get_fistname_lastname_pat(self, name: str):
        return await self.repo.get_author_fistname_latname_pat(name)
