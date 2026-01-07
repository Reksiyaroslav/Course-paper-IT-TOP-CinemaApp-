from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import RatingFilm, Film
from sqlalchemy import select,delete
from uuid import UUID
from typing import Dict
import datetime
from sqlalchemy.orm import selectinload


class RatingFilmRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ratingfilm(self, data: Dict, user_id: UUID, film_id: UUID):
        rating_film = RatingFilm(**data, user_id=user_id, film_id=film_id)
        self.session.add(rating_film)
        await self.session.commit()
        await self.session.refresh(rating_film)
        return rating_film
    async def get_ratings(self):
        smt =  select(RatingFilm)
        relult = await self.session.execute(smt)
        ratings = relult.scalars().all()
        return ratings 
    async def get_by_id_rating(self,rating_id):
        rating = await self.session.get(RatingFilm,rating_id)
        return rating
    async def delete_rating(self,rating_id):
        smt = delete(RatingFilm).where(RatingFilm.rating_id==rating_id)
        await self.session.execute(smt)
        await self.session.commit()
        return {"message":"Delete rating the db"}
    async def average_rating_film(self, film_id: UUID):
        smnt = select(Film).options(selectinload(Film.rating_films)).where(Film.film_id == film_id)
        relult = await self.session.execute(smnt)
        film = relult.scalars().one()
        ratings_film = film.rating_films
        average_rating:float = 0.0
        if ratings_film!= None:
            average_rating=1
            return average_rating
        for rating_film in ratings_film:
            average_rating += rating_film.rating
        average_rating /= len(film.rating_films)
        return average_rating
    async def update_rating(self, rating_id: UUID, data: dict):
        rating_film = self.get_by_id_rating(rating_id=rating_id)
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
    
    async def update_rating_user_id(self, user_id: UUID, data: dict):
        smnt = select(RatingFilm).where(RatingFilm.user_id == user_id)
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
