from app.service.base_service import Base_Service
from app.repositories.users_repositorie import UserRepository
from app.repositories.films_repositorie import FilmRepository
from uuid import UUID


class RatingFilmService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)

    async def create_ratingfilm(sefl, data: dict, user_id: UUID, film_id: UUID):
        return await sefl.repo.create_ratingfilm(data, user_id, film_id)

    async def average_rating_film(sefl, film_id: UUID):
        return await sefl.repo.average_rating_film(film_id)
