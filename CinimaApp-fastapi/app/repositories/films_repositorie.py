from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Film, RatingFilm, Coment
from sqlalchemy import select
from uuid import UUID
from app.repositories.actors_repositorie import ActorRepository
from app.repositories.repostoried import ModelRepository
from app.repositories.author_repositore import AuthorRepository


class FilmRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Film)

    async def add_actor(self, actor_id: UUID, film_id: UUID) -> Film | None:
        film = await self.get_model_id(film_id)
        if not film:
            return None
        actor_repo = ActorRepository(self.session)
        actor = await actor_repo.get_model_id(actor_id)
        if not any(a.id == actor_id for a in film.actors):
            film.actors.append(actor)

        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def add_author(self, author_id: UUID, film_id: UUID) -> Film | None:
        film = await self.get_model_id(film_id)
        if not film:
            return None
        author_repo = AuthorRepository(self.session)
        author = await author_repo.get_model_id(author_id)
        if not any(a.id == author_id for a in film.authors):
            film.authors.append(author)
        await self.session.commit()
        await self.session.refresh(film)
        return film

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

    async def add_list_actor_id(
        self, actor_ids: list[UUID], film_id: UUID
    ) -> Film | None:
        film = await self.get_model_id(film_id)
        if not film:
            return None

        actor_repo = ActorRepository(self.session)
        actors = []
        for actor_id in actor_ids:
            actor = await actor_repo.get_model_id(actor_id)
            if actor:
                actors.append(actor)
        not_actor_id = {a.id for a in film.actors}
        for actor in actors:
            if actor.id not in not_actor_id:
                film.actors.append(actor)

        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def add_list_author_id(
        self, author_ids: list[UUID], film_id: UUID
    ) -> Film | None:
        film = await self.get_model_id(film_id)
        if not film:
            return None
        author_repo = AuthorRepository(self.session)
        authors = []
        for author_id in author_ids:
            author = await author_repo.get_model_id(author_id)
            if author:
                authors.append(author)

        not_author_id = {a.id for a in film.authors}

        for author in authors:
            if author.id not in not_author_id:
                film.authors.append(author)
        await self.session.commit()
        await self.session.refresh(film)
        return film

    async def get_film_film_ids(self, film_ids: list[UUID]):
        smt = select(Film).where(Film.id.in_(film_ids))
        result = await self.session.execute(smt)
        return result.scalars().all()

    async def get_film_title(self, film_titel) -> Film:
        smt = select(Film).where(Film.title == film_titel)
        relutt = await self.session.execute(smt)
        films = relutt.scalars().first()
        return films

    async def get_list_actor(self, film_id: UUID):
        actor_repo = ActorRepository(self.session)
        film = await self.get_model_id(film_id)

        if not film:
            raise ValueError("Нету такого  фильма")
        actor_ids = [actor.id for actor in film.actors]
        list_actor = await actor_repo.get_list_actor_ids(actor_ids)
        return list_actor

    async def get_list_author(self, film_id: UUID):
        actor_repo = AuthorRepository(self.session)
        film = await self.get_model_id(film_id)
        if not film:
            raise ValueError("Нету такого  фильма")
        actor_ids = [author.id for author in film.authors]
        list_author = await actor_repo.get_list_author_ids(actor_ids)
        return list_author

    async def get_films_title_list(self, film_titel) -> list[Film]:
        smt = select(Film).where(Film.title == film_titel)
        relutt = await self.session.execute(smt)
        films = relutt.scalars().all()

        return films
