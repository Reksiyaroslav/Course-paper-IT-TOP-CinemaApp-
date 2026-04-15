from os import name
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List
from datetime import date
from app.db.model.model_db import (
    Film,
    RatingFilm,
    Coment,
    Actor,
    Author,
    TypeFilm,
    Country,
    film_type_film,
    film_actor,
    author_cinema,
)


class FilmRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_film(self, data: dict) -> Film | None:
        try:
            new_film = Film(**data)
            self.session.add(new_film)
            await self.session.commit()
            await self.session.refresh(new_film)
            return new_film
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(Exception(f"Error сreate film: {str(e)}"))
            return None

    async def get_film_by_id(self, film_id) -> Film | None:
        smt = (
            select(Film)
            .options(
                selectinload(Film.actors),
                selectinload(Film.authors),
                selectinload(Film.coments).selectinload(Coment.user),
                selectinload(Film.rating_films),
                selectinload(Film.types_film),
                selectinload(Film.country),
            )
            .filter(Film.film_id == film_id)
        )
        relult = await self.session.execute(smt)
        film = relult.scalars().first()
        return film

    async def update_film(self, film_id: UUID, data: dict) -> Film:
        try:
            film = await self.get_film_by_id(film_id)
            for key, value in data.items():
                if value is not None and hasattr(film, key):
                    setattr(film, key, value)
            await self.session.commit()
            await self.session.refresh(film)
            update_film = await self.get_film_by_id(film_id)
            return update_film
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error update film: {str(e)}")

    async def delete_film(self, film_id: UUID) -> bool:  # -> Any:
        try:
            smt = delete(Film).where(Film.film_id == film_id)
            relult = await self.session.execute(smt)
            await self.session.commit()
            return True
        except Exception:
            print(Exception)
            await self.session.rollback()
            return False

    async def get_films(self) -> List[Film]:
        smt = select(Film).options(
            selectinload(Film.actors),
            selectinload(Film.authors),
            selectinload(Film.coments),
            selectinload(Film.rating_films),
            selectinload(Film.types_film),
        )
        relult = await self.session.execute(smt)
        films = relult.scalars().all()
        return films

    async def update_rating(self, film_id: UUID, avg_rating: float) -> Film | str:
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return "Not db film"
        else:
            film.avg_rating = avg_rating
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def add_coment_film(self, film_id: UUID, coment: Coment) -> Film | None:
        film = await self.get_film_by_id(film_id)
        if film:
            film.coments.append(coment)
            await self.session.commit()
            await self.session.refresh(film)
        else:
            raise ValueError("Not filem ")

    async def add_ratingfilm_film(
        self, film_id: UUID, ratingfilm: RatingFilm
    ) -> Film | None:
        if not ratingfilm:
            raise ValueError("rating none")
        film = await self.get_film_by_id(film_id)
        if film:
            film.rating_films.append(ratingfilm)
            await self.session.commit()
            await self.session.refresh(film)
        else:
            raise ValueError("Not filem ")

    async def add_list_actor_id(
        self, actor_ids: list[UUID], film_id: UUID
    ) -> Film | None:
        film = await self.get_film_by_id(film_id)
        if not film:
            return None
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

    async def add_list_author_id(
        self, author_ids: list[UUID], film_id: UUID
    ) -> Film | None:
        film = await self.get_film_by_id(film_id)
        if not film:
            return None
        exit_author_ids = [author.author_id for author in film.authors]
        stmt = select(Author).where(Author.author_id.in_(author_ids))
        relult = await self.session.execute(stmt)
        new_authors = relult.scalars().all()
        for author in new_authors:
            if author.author_id not in exit_author_ids:
                film.authors.append(author)
        await self.session.commit()
        await self.session.refresh(film)

        return film

    async def add_types_film(self, types_film_id: List[UUID], film_id: UUID):
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        smt = select(TypeFilm).where(TypeFilm.type_film_id.in_(types_film_id))
        relult = await self.session.execute(smt)
        new_type_film = relult.scalars().all()
        types_film = [type_film.type_film_id for type_film in film.types_film]
        for type_film in new_type_film:
            if type_film.type_film_id not in types_film:
                film.types_film.append(type_film)
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def add_country(self, country_id: UUID, film_id: UUID):
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        smt = select(Country).where(Country.country_id == country_id)
        relult = await self.session.execute(smt)
        country = relult.scalars().first()
        if not country:
            return None
        film.country = country
        film.country_id = country.country_id
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def set_type_film(self, types_film_id: List[UUID], film_id: UUID):
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        old_types_film = [type_film.type_film_id for type_film in film.types_film]
        delete_type_film = []
        add_type_film = []
        for new_type_id in types_film_id:
            if new_type_id not in old_types_film:
                add_type_film.append(new_type_id)
        for old_type_film_id in old_types_film:
            if old_type_film_id not in types_film_id:
                delete_type_film.append(old_type_film_id)
        if len(add_type_film) == 0 and len(delete_type_film) == 0:
            print("Нет изменеий ")
            return film
        if len(delete_type_film) > 0:
            smt = delete(film_type_film).where(
                and_(
                    film_type_film.c.film_id == film_id,
                    film_type_film.c.type_film_id.in_(delete_type_film),
                )
            )
            await self.session.execute(smt)
        if len(add_type_film) > 0:
            smt = select(TypeFilm).where(TypeFilm.type_film_id.in_(add_type_film))
            relult = await self.session.execute(smt)
            update_type_films = relult.scalars().all()
            for update_type_film in update_type_films:
                film.types_film.append(update_type_film)
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def set_actors(self, actors_id: List[UUID], film_id: UUID):
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        old_actors_id = [actor.actor_id for actor in film.actors]
        add_actors = []
        delete_actors = []
        for new_actor_id in actors_id:
            if new_actor_id not in old_actors_id:
                add_actors.append(new_actor_id)

        for old_actor_id in old_actors_id:
            if old_actor_id not in actors_id:
                delete_actors.append(old_actor_id)
        if len(add_actors) == 0 and len(delete_actors) == 0:
            print("Нет изменеий ")
            return film
        if len(delete_actors) > 0:
            smt = delete(film_actor).where(
                and_(
                    film_actor.c.film_id == film_id,
                    film_actor.c.actor_id.in_(delete_actors),
                )
            )
            await self.session.execute(smt)
        if len(add_actors) > 0:
            smt = select(Actor).where(Actor.actor_id.in_(add_actors))
            relult = await self.session.execute(smt)
            update_actors = relult.scalars().all()
            for update_actor in update_actors:
                film.actors.append(update_actor)
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def set_auhtors(self, authors_id: List[UUID], film_id: UUID):
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        old_author_ids = [author.author_id for author in film.authors]
        add_authors = []
        delete_authors = []
        for new_author_id in authors_id:
            if new_author_id not in old_author_ids:
                add_authors.append(new_author_id)

        for old_author_id in old_author_ids:
            if old_author_id not in authors_id:
                delete_authors.append(old_author_id)
        if len(add_authors) == 0 and len(delete_authors) == 0:
            print("Нет изменеий ")
            return film
        if len(delete_authors) > 0:
            smt = delete(author_cinema).where(
                and_(
                    author_cinema.c.film_id == film_id,
                    author_cinema.c.author_id.in_(delete_authors),
                )
            )
            await self.session.execute(smt)
        if len(add_authors) > 0:
            smt = select(Author).where(Author.author_id.in_(add_authors))
            relult = await self.session.execute(smt)
            update_authors = relult.scalars().all()
            for update_author in update_authors:
                film.authors.append(update_author)
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def set_country(self, country_id: UUID, film_id: UUID):
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        smt = select(Country).where(Country.country_id == country_id)
        relult = await self.session.execute(smt)
        country = relult.scalars().first()
        if not country:
            return None
        if film.country_id == country.country_id:
            return film
        film.country = country
        film.country_id = country.country_id
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def get_film_film_ids(self, film_ids: list[UUID]) -> List[Film]:
        smt = select(Film).where(Film.film_id.in_(film_ids))
        result = await self.session.execute(smt)
        return list(result.scalars().all())

    async def get_film_block(self) -> list[Film]:
        """Для вывода только части информаций по фильма"""
        smt = select(
            Film.film_id,
            Film.title,
            Film.description,
            Film.path_image,
            Film.avg_rating,
            Film.release_date,
        )
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
            film.release_date = row[5]
            film_list.append(film)
        return film_list

    async def get_doble_title(self, title: str, film_id: UUID):
        if not title or title.strip():
            return False
        clean_title = title.strip().lower()
        smt = select(Film).where(
            and_(Film.film_id != film_id, func.lower(Film.title) == clean_title)
        )
        relutt = await self.session.execute(smt)
        films = relutt.scalars().first() is not None
        return films

    async def get_film_title(self, film_titel) -> Film | None:
        """Получения данных по фильма с одинаковым или похожим названиям"""
        smt = select(Film).where(Film.title.ilike(f"%{film_titel}%"))
        relutt = await self.session.execute(smt)
        films = relutt.scalars().all()
        if not films:
            return None
        return films

    async def get_film_ratings_date_country_type_film(
        self,
        min_rating: float = None,
        max_rating: float = None,
        country_name: str = None,
        type_film: list[str] = None,
        min_date: date = None,
        max_date: date = None,
    ):
        "Для поиска фильмов по коретным требованием"
        smt = select(Film)
        pravila: list = []
        if min_rating is not None and min_rating > 0.0:
            pravila.append(Film.avg_rating >= min_rating)
        if max_rating is not None and max_rating > 0.0:
            pravila.append(Film.avg_rating <= max_rating)
        if country_name is not None and len(country_name) >= 3:
            smt = smt.join(Film.country)
            pravila.append(func.lower(Country.country_name) == country_name.lower())
        if type_film:
            pravila.append(Film.types_film.any(TypeFilm.type_film_name.in_(type_film)))
        if min_date:
            pravila.append(Film.release_date >= min_date)
        if max_date:
            pravila.append(Film.release_date <= max_date)
        if pravila:
            smt = smt.where(*pravila)
        relut = await self.session.execute(smt)
        films = relut.scalars().all()
        return films

    async def get_list_actor(self, film_id: UUID) -> List[Actor] | None:
        """Получение информаций о сценаристов фильма кто занимался"""
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        return film.actors

    async def get_list_author(self, film_id: UUID) -> List[Author] | None:
        """Актёры которые смнимальс там"""
        film = await self.get_film_by_id(film_id=film_id)
        if not film:
            return None
        return film.authors

    async def get_list_coment(self, film_id: UUID) -> List[Coment] | None:
        """Получения все кометариях о фильме"""
        film = await self.get_film_by_id(film_id)
        if not film:
            return None
        return film.coments

    async def get_list_rating(self, film_id: UUID) -> List[RatingFilm] | None:
        """Получения информаций о ратингах фильма"""
        film = await self.get_film_by_id(film_id)
        if not film:
            return None
        return film.rating_films
