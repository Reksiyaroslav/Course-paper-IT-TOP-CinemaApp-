from app.service.base_service import Base_Service
from app.repositories.users_repositorie import UserRepository
from app.repositories.films_repositorie import FilmRepository
from uuid import UUID


class RatingFilmService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)
        self.user_repo = UserRepository(self.repo.session)
        self.film_repo = FilmRepository(self.repo.session)

    async def create_model(self, data, name_title_value=None):
        old_rating = await self.repo.get_user_film_rating(
            data["film_id"], data["user_id"]
        )
        if old_rating:
            updated_rating = await self.add_update_film_and_user(
                data["film_id"], data["user_id"], data["rating"]
            )
            return updated_rating

        else:
            rating = await super().create_model(data, name_title_value)

            # Проверяем, что объект создан
            if rating is None:
                print("Данные для создания рейтинга:", data)
                raise ValueError("Ошибка создания рейтинга: объект не был создан")

            await self.film_repo.add_ratingfilm_film(data["film_id"], rating)
            await self.user_repo.add_ratingfilm_user(data["user_id"], rating)
            return rating

    async def add_update_film_and_user(self, film_id: UUID, user_id: UUID, rating):
        ratingfilm = await self.repo.add_upadate_rating_user_and_film(
            film_id, user_id, rating
        )
        await self.film_repo.add_ratingfilm_film(film_id, ratingfilm)
        await self.user_repo.add_ratingfilm_user(user_id, ratingfilm)
        return ratingfilm

    async def get_list_film_rating(self, film_id: UUID):
        return await self.repo.get_list_film_rating(film_id)

    async def get_list_user_rating(self, user_id: UUID):
        return await self.repo.get_list_user_rating(user_id)
