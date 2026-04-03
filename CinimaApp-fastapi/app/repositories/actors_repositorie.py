from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Actor, uuid, Country
from sqlalchemy import select, or_, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError


class ActorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_actor(self, data: dict) -> Actor | None:
        "Создание актёра"
        try:
            actor = Actor(**data)
            self.session.add(actor)
            await self.session.commit()
            return actor
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(e)
            return None

    async def get_actors(self) -> list[Actor] | None:
        "Получения списка актеров"
        try:
            smt = select(Actor)
            relult = await self.session.execute(smt)
            actor = relult.scalars().all()
            return actor
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise

    async def get_actor_by_id(self, actor_id: uuid.UUID) -> Actor | None:
        "Получение актера по id"
        smt = (
            select(Actor)
            .options(selectinload(Actor.films_acted), selectinload(Actor.country))
            .where(Actor.actor_id == actor_id)
        )
        relult = await self.session.execute(smt)
        actor = relult.scalars().first()
        return actor

    async def update_actor(self, data: dict, actor_id: uuid.UUID):
        "Обновления актёра"
        actor = await self.get_actor_by_id(actor_id=actor_id)
        if not actor:
            return None
        for key, values in data.items():
            if values is not None and hasattr(actor, key):
                setattr(actor, key, values)
        await self.session.commit()
        await self.session.refresh(actor)
        return actor

    async def delete_actor(self, actor_id: uuid.UUID) -> bool:
        "Удаланения актёра"
        try:
            smt = delete(Actor).filter(Actor.actor_id == actor_id)
            result = await self.session.execute(smt)
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False

    async def add_country(self, actor_id: uuid.UUID, country_id: uuid.UUID):
        actor = await self.get_actor_by_id(actor_id=actor_id)
        if not actor:
            return None
        smt = select(Country).where(Country.country_id == country_id)
        relult = await self.session.execute(smt)
        country = relult.scalars().first()
        if not country:
            return actor
        actor.country = country
        actor.country_id = country.country_id
        await self.session.commit()
        await self.session.refresh(actor)
        return actor

    async def set_country(self, actor_id: uuid.UUID, country_id: uuid.UUID):
        actor = await self.get_actor_by_id(actor_id=actor_id)
        if not actor:
            return None
        smt = select(Country).where(Country.country_id == country_id)
        relult = await self.session.execute(smt)
        country = relult.scalars().first()
        if not country:
            return actor
        if actor.country_id == country.country_id:
            return actor
        actor.country = country
        actor.country_id = country.country_id
        await self.session.commit()
        await self.session.refresh(actor)
        return actor

    async def get_duble_actor(self, actor_id: uuid.UUID, fistname):
        pass

    async def get_actorname_list(self, name: str) -> list[Actor] | None:
        "Получения актеров по имени или очеству которые совпадают"
        serhat_parametr = f"%{name}%"
        smt = select(Actor).where(
            or_(
                Actor.fistname.contains(serhat_parametr),
                Actor.lastname.contains(serhat_parametr),
                Actor.patronymic.contains(serhat_parametr),
            )
        )
        result = await self.session.execute(smt)
        actors = result.scalars().all()
        if not actors:
            return None
        return actors
