from app.service.base_service import Base_Service
from uuid import UUID
from app.repositories.ratingfilm_repositore import (
    RatingFilmRepository,
    RatingFilm as rating_model,
)
from app.utils.comon import not_create_rating


class RatingFilmService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.rating_repo = RatingFilmRepository(self.session)

    async def create_ratingfilm(
        self, data: dict, user_id: UUID, film_id: UUID
    ) -> dict | rating_model:
        if not await not_create_rating(
            session=self.session, model=rating_model, user_id=user_id, film_id=film_id
        ):
            return {"message": "Не возможо создать такую ратин он у вас есть"}
        else:
            return await self.rating_repo.create_ratingfilm(data, user_id, film_id)

    async def average_rating_film(self, film_id: UUID) -> int:
        return await self.rating_repo.average_rating_film(film_id)

    async def get_by_id_rating(self, rating_id) -> rating_model:
        return await self.rating_repo.get_by_id_rating(rating_id=rating_id)

    async def get_list_rating(self) -> list[rating_model]:
        return await self.rating_repo.get_ratings()

    async def delete_rating(self, rating_id):
        return await self.rating_repo.delete_rating(rating_id=rating_id)

    async def update_rating_user_id_and_film_id(
        self, data: dict, user_id: UUID, film_id: UUID
    ) -> rating_model:
        return await self.rating_repo.update_rating_user_id(
            user_id=user_id, data=data, film_id=film_id
        )

    async def update_rating(self, rating_id, data: dict):
        return await self.rating_repo.update_rating(data=data, rating_id=rating_id)
