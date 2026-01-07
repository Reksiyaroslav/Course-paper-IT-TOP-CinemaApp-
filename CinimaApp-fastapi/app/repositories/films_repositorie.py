from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import (
    Film,
    RatingFilm,
    Coment,
    Actor,
    Author
)
from sqlalchemy import select,delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from uuid import UUID
class FilmRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_film(self,data:dict)->dict:
        self.session.add(Film(**data))
        await self.session.commit()
        return {"message":"Create film good"}
    
    async def get_film_by_id(self,film_id):
        smt = select(Film).options(
                selectinload(Film.actors),
                selectinload(Film.authors),
                selectinload(Film.coments),
                selectinload(Film.rating_films),
            ).filter(Film.film_id==film_id)
        relult = await self.session.execute(smt)
        film = relult.scalars().first()
        return film
    
    async def update_film(self, film_id: UUID, data: dict) ->Film:
        try:
            film = await self.get_film_by_id(film_id)
            for key, value in data.items():
                if value is not None and hasattr(film, key):
                    setattr(film, key, value)
            await self.session.commit()
            await self.session.refresh(film)
            update_film =await  self.get_film_by_id(film_id)
            return update_film
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error update film: {str(e)}")
        
    async def delete_film(self,film_id):# -> Any:
        smt = delete(Film).where(Film.film_id==film_id)
        await self.session.execute(smt)
        await self.session.commit()
        return None 
    
    async def get_films(self):
        smt = select(Film).options(
                selectinload(Film.actors),
                selectinload(Film.authors),
                selectinload(Film.coments),
                selectinload(Film.rating_films),
            )
        relult = await self.session.execute(smt)
        film = relult.scalars().all()
        return film
    async def update_rating(self,film_id:UUID,avg_rating:float):
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return "Not db film"
        else:
            film.avg_rating = avg_rating
        await self.session.commit()
        await self.session.refresh(film)
        return film
    async def add_coment_film(self, film_id: UUID, coment: Coment):
        film = await self.get_film_by_id(film_id)
        if film:
            film.films_comnet.append(coment)
            await self.session.commit()
            await self.session.refresh(film)
        else:
            raise ValueError("Not filem ")

    async def add_ratingfilm_film(self, film_id: UUID, ratingfilm: RatingFilm):
        if not ratingfilm:
            raise ValueError("rating nmone")
        film = await self.get_film_by_id(film_id)
        if film:
            film.rating_films.append(ratingfilm)
            await self.session.commit()
            await self.session.refresh(film)
        else:
            raise ValueError("Not filem ")

    async def add_list_actor_id(self, actor_ids: list[UUID], film_id: UUID) -> Film|None:
        film = await self.get_film_by_id(film_id)
        exit_actor_ids = [actor.actor_id for actor in film.actors]
        stmt = select(Actor).where(Actor.actor_id.in_(actor_ids))
        relult = await self.session.execute(stmt)
        new_actors = relult.scalars().all()
        for actor in new_actors:
            if actor.actor_id not in exit_actor_ids:
                film.actors.append(actor)
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def add_list_author_id(self, author_ids:list[ UUID], film_id: UUID) -> Film|None:
        film = await self.get_film_by_id(film_id)
        exit_author_ids = [author.author_id for author in film.authors]
        stmt = select(Author).where(Author.author_id.in_(author_ids))
        relult = await self.session.execute(stmt)
        new_authors = relult.scalars().all()
        for author in new_authors:
            if author.author_id not in exit_author_ids:
                film.authors.append(author)
        await self.session.commit()
        await self.session.refresh(film)
        if not film:
            return None
        return film

    async def get_film_film_ids(self, film_ids: list[UUID]):
        smt = select(Film).where(Film.film_id.in_(film_ids))
        result = await self.session.execute(smt)
        return result.scalars().all()
    
    async def get_film_block(self)->list[Film]:
        """Для вывода только части информаций по фильма"""
        smt = select(Film.film_id,Film.title,Film.description,Film.path_image,Film.avg_rating)
        result = await self.session.execute(smt)
        rows = result.all()
        film_list = []
       

        for row in rows:
            film = Film() 
            film.film_id = row[0]
            film.title = row[1]
            film.description = row[2]
            film.path_image = row[3]
            film.avg_rating = row[4]
            film_list.append(film)
        return film_list
    
    async def get_film_title(self, film_titel, limint: int) -> Film| None:
        """Получения данных по фильма с одинаковым или похожим названиям"""
        smt = select(Film).where(Film.title.ilike(f"%{film_titel}%")).limit(limint)
        relutt = await self.session.execute(smt)
        films = relutt.scalars().first()
        if not films:
            return None
        return films

    async def get_list_actor(self, film_id: UUID):
        """Получение информаций о сценаристов фильма кто занимался """
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        return film.actors

    async def get_list_author(self, film_id: UUID):
        """Актёры которые смнимальс там"""
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        return film.authors

    async def get_list_coment(self, film_id: UUID):
        """Получения все кометариях о фильме """
        film = await self.get_film_by_id(film_id)
        if not film:
            return None
        return film.coments

    async def get_list_rating(self, film_id: UUID):
        """Получения информаций о ратингах фильма """
        film = await self.get_film_by_id(film_id)
        if not film:
            return None
        return film.rating_films
