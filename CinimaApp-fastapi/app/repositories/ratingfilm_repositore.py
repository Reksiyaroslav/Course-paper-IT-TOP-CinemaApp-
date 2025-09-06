from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import RatingFilm, Film
from sqlalchemy import select, delete, update
from uuid import UUID
from app.repositories.repostoried import ModelRepository
from typing import Dict
import datetime


class RatingFilmRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=RatingFilm)

    async def create_ratingfilm(self, data: Dict, user_id: UUID, film_id: UUID):
        rating_film = RatingFilm(**data, user_id=user_id, film_id=film_id)
        self.session.add(rating_film)
        await self.session.commit()
        await self.session.refresh(rating_film)
        return rating_film

    async def average_rating_film(self, film_id: UUID):
        smnt = select(Film).where(Film.id == film_id)
        relult = await self.session.execute(smnt)
        film = relult.scalars().one()
        ratings_film = film.rating_films
        average_rating = 0
        for rating_film in ratings_film:
            average_rating += rating_film.rating
        average_rating /= len(film.rating_films)
        return average_rating
    async def update_rating_user_id(self, user_id:UUID, data:dict):
        smnt = select(RatingFilm).where(RatingFilm.user_id==user_id)
        relult = await self.session.execute(smnt)
        rating_film = relult.scalars().one()
        if not rating_film:
            return None
        for key,value in  data.items():
            if value is not None and hasattr(rating_film, key):
                    setattr(rating_film, key, value)
            if hasattr(rating_film, "update_at"):
                setattr(rating_film, "update_at", datetime.datetime.utcnow())

        await self.session.commit()
        await self.session.refresh(rating_film)
        return rating_film
        
           

