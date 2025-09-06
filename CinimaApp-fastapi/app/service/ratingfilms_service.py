from app.service.base_service import Base_Service
from app.repositories.users_repositorie import UserRepository
from app.repositories.films_repositorie import FilmRepository
from uuid import UUID


class RatingFilmService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)

    async def create_ratingfilm(self, data: dict, user_id: UUID, film_id: UUID):
        return await self.repo.create_ratingfilm(data, user_id, film_id)

    async def average_rating_film(self, film_id: UUID):
        return await self.repo.average_rating_film(film_id)
    async def update_rating_user_id(self,data:dict,user_id:UUID):
        return await self.repo.update_rating_user_id(user_id,data)