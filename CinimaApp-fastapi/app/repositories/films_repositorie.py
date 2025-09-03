from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import (
    Film,
    RatingFilm,
    Coment,
    Actor,
    Author,
    film_actor,
    author_ciema,
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.repositories.repostoried import ModelRepository


class FilmRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Film)

    async def add_coment_film(self, film_id: UUID, coment: Coment):
        film = await self.get_model_id(film_id)
        if film:
            film.films_comnet.append(coment)
            await self.session.commit()
            await self.session.refresh(film)
        else:
            raise ValueError("Not filem ")

    async def add_ratingfilm_film(self, film_id: UUID, ratingfilm: RatingFilm):
        if not ratingfilm:
            raise ValueError("rating nmone")
        film = await self.get_model_id(film_id)
        if film:
            film.rating_films.append(ratingfilm)
            await self.session.commit()
            await self.session.refresh(film)
        else:
            raise ValueError("Not filem ")

    async def get_film_relations(self, film_id: UUID):
        stmt = (
            select(Film)
            .where(Film.id == film_id)
            .options(selectinload(Film.actors), selectinload(Film.authors))
        )
        relult = await self.session.execute(stmt)
        return relult.scalar_one_or_none()

    async def add_list_actor_id(
        self, actor_ids: list[UUID], film_id: UUID
    ) -> Film | None:
        film = await self.get_film_relations(film_id)
        if not film:
            return None
        exit_actor_ids = [actor.id for actor in film.actors]
        stmt = select(Actor).where(Actor.id.in_(actor_ids))
        relult = await self.session.execute(stmt)
        new_actors = relult.scalars().all()
        for actor in new_actors:
            if actor.id not in exit_actor_ids:
                film.actors.append(actor)
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def add_list_author_id(
        self, author_ids: list[UUID], film_id: UUID
    ) -> Film | None:
        film = await self.get_film_relations(film_id)
        if not film:
            return None
        exit_author_ids = [author.id for author in film.authors]
        stmt = select(Author).where(Author.id.in_(author_ids))
        relult = await self.session.execute(stmt)
        new_authors = relult.scalars().all()
        for author in new_authors:
            if author.id not in exit_author_ids:
                film.authors.append(author)

        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def get_film_film_ids(self, film_ids: list[UUID]):
        smt = select(Film).where(Film.id.in_(film_ids))
        result = await self.session.execute(smt)
        return result.scalars().all()

    async def get_film_title(self, film_titel, limint: int) -> Film:
        smt = select(Film).where(Film.title.ilike(f"%{film_titel}%")).limit(limint)
        relutt = await self.session.execute(smt)
        films = relutt.scalars().first()
        return films

    async def get_list_actor(self, film_id: UUID):
        film = await self.get_film_relations(film_id=film_id)
        return film.actors

    async def get_list_author(self, film_id: UUID):
        film = await self.get_film_relations(film_id=film_id)
        return film.authors

    async def get_films_title_list(self, film_titel) -> list[Film]:
        smt = select(Film).where(Film.title == film_titel)
        relutt = await self.session.execute(smt)
        films = relutt.scalars().all()

        return films
