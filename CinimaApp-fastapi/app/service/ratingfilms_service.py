from app.service.base_service import Base_Service
from uuid import UUID
from app.repositories.ratingfilm_repositore import RatingFilmRepository

class RatingFilmService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.rating_repo = RatingFilmRepository(self.session)
    async def create_ratingfilm(self, data: dict, user_id: UUID, film_id: UUID):
        return await self.rating_repo.create_ratingfilm(data, user_id, film_id)

    async def average_rating_film(self, film_id: UUID):
        return await self.rating_repo.average_rating_film(film_id)
    async def get_by_id_rating(self,rating_id):
        return await self.rating_repo.get_by_id_rating(rating_id=rating_id)
    async def get_list_rating(self):
        return await self.rating_repo.get_ratings()
    async def delete_rating(self,rating_id):
        return await self.rating_repo.delete_rating(rating_id=rating_id)
    async def update_rating_user_id(self, data: dict, user_id: UUID):
        return await self.rating_repo.update_rating_user_id(user_id, data)
    async def update_rating(self,rating_id,data:dict):
        return await self.rating_repo.update_rating(data=data,rating_id=rating_id)
