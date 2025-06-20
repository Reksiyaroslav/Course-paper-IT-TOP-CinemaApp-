from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model_db.model_db import Actor
from sqlalchemy import select, delete
from app.repositories.repostoried import ModelRepository
import uuid


class ActorRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Actor)

    async def get_actorname(self, actorname: str) -> Actor:
        smt = select(Actor).where(
            (Actor.fistName == actorname)
            | (Actor.lastName == actorname)
            | (Actor.patronymic == actorname)
        )
        result = await self.session.execute(smt)
        actor = result.scalars().first()
        return actor

    async def get_actorname_list(self, actorname: str) -> Actor:
        smt = select(Actor).where(
            (Actor.fistName == actorname)
            | (Actor.lastName == actorname)
            | (Actor.patronymic == actorname)
        )
        result = await self.session.execute(smt)
        actor = result.scalars().all()
        return actor

    async def get_list_actor_ids(self, actor_ids: uuid.UUID):
        smt = select(Actor).where(Actor.id.in_(actor_ids))
        relut = await self.session.execute(smt)
        list_actor = relut.scalars().all()
        return list_actor
