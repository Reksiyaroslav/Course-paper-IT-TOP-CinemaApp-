from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import RatingFilm, Film
from sqlalchemy import select, delete, and_
from uuid import UUID
from typing import Dict, List
import datetime
from sqlalchemy.orm import selectinload


class RatingFilmRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ratingfilm(
        self, data: Dict, user_id: UUID, film_id: UUID
    ) -> RatingFilm:
        "Создание ратинаг"
        try:
            rating_film = RatingFilm(**data, user_id=user_id, film_id=film_id)
            self.session.add(rating_film)
            await self.session.commit()
            await self.session.refresh(rating_film)
            return rating_film
        except Exception as e:
            await self.session.rollback()
            print(f"Error create_rating: {e}")
            return None

    async def get_ratings(self) -> List[RatingFilm]:
        "Получения всеех ратинга"
        smt = select(RatingFilm)
        relult = await self.session.execute(smt)
        ratings = relult.scalars().all()
        return ratings

    async def get_rating_user_id_and_film(
        self, user_id: UUID, film_id: UUID
    ) -> RatingFilm:
        smt = select(RatingFilm).where(
            and_(RatingFilm.film_id == film_id, RatingFilm.user_id == user_id)
        )
        relult = await self.session.execute(statement=smt)
        rating = relult.scalars().first()
        return rating

    async def get_by_id_rating(self, rating_id: UUID) -> RatingFilm | None:
        "Получения ратинга id"
        rating = await self.session.get(RatingFilm, rating_id)
        return rating

    async def delete_rating(self, rating_id: UUID) -> bool:
        try:
            smt = delete(RatingFilm).where(RatingFilm.rating_id == rating_id)
            result = await self.session.execute(smt)
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False

    async def average_rating_film(self, film_id: UUID) -> float:
        smnt = (
            select(Film)
            .options(selectinload(Film.rating_films))
            .where(Film.film_id == film_id)
        )
        relult = await self.session.execute(smnt)
        film = relult.scalars().one_or_none()
        average_rating: float = 0.0
        if not film or not film.rating_films:
            return average_rating
        total = sum(rating.rating for rating in film.rating_films)
        count = len(film.rating_films)
        average_rating = round(total / count, 2)
        return average_rating

    async def update_rating(self, rating_id: UUID, data: dict) -> RatingFilm | None:
        rating_film = await self.get_by_id_rating(rating_id=rating_id)
        if not rating_film:
            return None
        for key, value in data.items():
            if value is not None and hasattr(rating_film, key):
                setattr(rating_film, key, value)
            if hasattr(rating_film, "update_at"):
                setattr(rating_film, "update_at", datetime.datetime.utcnow())

        await self.session.commit()
        await self.session.refresh(rating_film)
        return rating_film

    async def update_rating_user_id(
        self, user_id: UUID, film_id: UUID, data: dict
    ) -> None | RatingFilm:
        smnt = select(RatingFilm).where(
            RatingFilm.user_id == user_id, RatingFilm.film_id == film_id
        )
        relult = await self.session.execute(smnt)
        rating_film = relult.scalars().one()
        if not rating_film:
            return None
        for key, value in data.items():
            if value is not None and hasattr(rating_film, key):
                setattr(rating_film, key, value)
            if hasattr(rating_film, "update_at"):
                setattr(rating_film, "update_at", datetime.datetime.utcnow())

        await self.session.commit()
        await self.session.refresh(rating_film)
        return rating_film
