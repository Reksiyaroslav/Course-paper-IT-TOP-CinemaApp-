from app.service.base_service import Base_Service
from app.repositories.users_repositorie import UserRepository
from app.repositories.films_repositorie import FilmRepository
from uuid import UUID
class ComentService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)
        self.user_repo = UserRepository(self.repo.session)
        self.film_repo = FilmRepository(self.repo.session)
    async def create_model(self, data, name_title_value=None):
        coment = await self.repo.create_coment(data)
        await self.film_repo.add_coment_film(data["film_id"],coment)
        await self.user_repo.add_coment_film(data["user_id"],coment)
        return coment
    async def list_user_coments(self,user_id:UUID):
        return await self.repo.list_user_coments(user_id)
    async def list_film_coments(self,film_id:UUID):
        return await self.repo.list_film_coments(film_id)
    