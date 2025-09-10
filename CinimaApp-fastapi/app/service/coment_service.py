from app.service.base_service import Base_Service

from uuid import UUID
from app.utils.comon import validet_text_coment
from fastapi.exceptions import HTTPException

class ComentService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)

    async def create_model(
        self,
        data,
        film_id: list[UUID],
        user_id: list[UUID],
        name_title_value=None,
    ):
        if not await   validet_text_coment(data,"description"):
            raise HTTPException(detail="Использовали не нужное слова в тексте",status_code=404)
            
        return await self.repo.create_coment(data, film_id, user_id)

    async def list_user_coments(self, user_id: UUID):
        return await self.repo.list_user_coments(user_id)

    async def update_like(self, coment_id: UUID):
        return await self.repo.update_like(coment_id)

    async def update_unlike(self, coment_id: UUID):
        return await self.repo.update_unlike(coment_id)

    async def list_film_coments(self, film_id: UUID):
        return await self.repo.list_film_coments(film_id)
