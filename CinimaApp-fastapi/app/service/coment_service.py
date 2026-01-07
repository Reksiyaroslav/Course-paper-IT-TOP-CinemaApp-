from app.service.base_service import Base_Service
from app.repositories.coment_repositoried import ComentRepository 
from uuid import UUID
from app.utils.comon import validet_text_coment
from fastapi.exceptions import HTTPException


class ComentService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.coment_repo = ComentRepository(self.session)

    async def create_model(
        self,
        data,
        film_id: UUID,
        user_id: UUID,
        name_title_value=None,
    ):
        if not await validet_text_coment(data, "description"):
            raise HTTPException(
                detail="Использовали не нужное слова в тексте", status_code=404
            )

        return await self.coment_repo.create_coment(data, film_id, user_id)
    async def get_coments(self):
        return await self.coment_repo.get_coments()
    async def get_by_id_coment(self,coment_id):
        return await self.coment_repo.get_by_id_coments(coment_id)
    async def update_coment(self,coment_id,data):
        if not await validet_text_coment(data, "description"):
            raise HTTPException(
                detail="Использовали не нужное слова в тексте", status_code=404
            )
        return await self.coment_repo.update_coment(coment_id =coment_id,data=data)
    async def delete_coment(self,coment_id):
        return await self.coment_repo.delete_coment(coment_id=coment_id)
    async def list_user_coments(self, user_id: UUID):
        return await self.coment_repo.list_user_coments(user_id)

    async def update_like(self, coment_id: UUID):
        return await self.coment_repo.update_like(coment_id)

    async def update_unlike(self, coment_id: UUID):
        return await self.coment_repo.update_unlike(coment_id)

    async def list_film_coments(self, film_id: UUID):
        return await self.coment_repo.list_film_coments(film_id)
