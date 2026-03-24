from uuid import UUID
from fastapi import HTTPException, status
from app.service.base_service import Base_Service

from app.utils.comon import not_create_rating
from app.scheme.rating.model_ratingfilms import (
    RatingFilmResponse,
    RatingFilmList,
    RatingFilmListAdmin,
)
from app.service.film_service import FilmService, RatingFilmRepository, rating_model


class RatingFilmService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.rating_repo = RatingFilmRepository(self.session)
        self.service_film: FilmService = FilmService(session)

    async def create_ratingfilm(
        self, data: dict, user_id: UUID, film_id: UUID
    ) -> dict | RatingFilmResponse:
        if await not_create_rating(
            session=self.session, model=rating_model, user_id=user_id, film_id=film_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Вы уже оценили этот фильм"
            )
        else:
            rating = await self.rating_repo.create_ratingfilm(data, user_id, film_id)
            await self.service_film.update_rating(film_id=film_id)
            return RatingFilmResponse.from_orm(rating)

    async def average_rating_film(self, film_id: UUID) -> float:
        average: float = await self.rating_repo.average_rating_film(film_id)
        return average

    async def get_by_id_rating(self, rating_id) -> RatingFilmResponse:
        rating = await self.rating_repo.get_by_id_rating(rating_id=rating_id)
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Рейтинг не найден"
            )
        return RatingFilmResponse.from_orm(rating)

    async def get_by_user_id_and_film_id(
        self, user_id, film_id
    ) -> RatingFilmResponse | None:
        rating = await self.rating_repo.get_rating_user_id_and_film(
            user_id=user_id, film_id=film_id
        )
        if not rating:
            return None
        return RatingFilmResponse.from_orm(rating)

    async def get_list_rating(self) -> RatingFilmList:
        ratings = await self.rating_repo.get_ratings()
        return RatingFilmList(rating_list=ratings)

    async def get_list_rating_admin(self) -> RatingFilmListAdmin:
        ratings = await self.rating_repo.get_ratings()
        return RatingFilmListAdmin(rating_list=ratings)

    async def delete_rating(self, rating_id, film_id):
        delete_rating = await self.rating_repo.delete_rating(rating_id=rating_id)
        if not delete_rating:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ратинг")
        await self.service_film.update_rating(film_id=film_id)
        return {"message": "Ратинг успешно удалён"}

    async def update_rating_user_id_and_film_id(
        self, data: dict, user_id: UUID, film_id: UUID
    ) -> RatingFilmResponse:
        rating = await self.rating_repo.update_rating_user_id(
            user_id=user_id, data=data, film_id=film_id
        )
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Рейтинг не найден"
            )
        await self.service_film.update_rating(film_id=film_id)
        return RatingFilmResponse.from_orm(rating)

    async def update_rating(self, rating_id, data: dict):
        update_rating = await self.rating_repo.update_rating(
            data=data, rating_id=rating_id
        )
        await self.service_film.update_rating(film_id=update_rating.film_id)
        return RatingFilmResponse.from_orm(update_rating)
