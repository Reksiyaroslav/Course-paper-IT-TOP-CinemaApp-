from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Actor
from sqlalchemy import select, delete
from app.repositories.repostoried import ModelRepository
import uuid


class ActorRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Actor)

    async def get_actorname(self, actorname: str) -> Actor:
        smt = select(Actor).where(
            (Actor.fistname == actorname)
            | (Actor.lastname == actorname)
            | (Actor.patronymic == actorname)
        )
        result = await self.session.execute(smt)
        actor = result.scalars().first()
        return actor

    async def get_actorname_list(self, name: str) -> Actor:
        smt = select(Actor).where(
            (Actor.fistname.ilike(f"%{name}%"))
            | (Actor.lastname.ilike(f"%{name}%"))
            | (Actor.patronymic.ilike(f"%{name}%"))
        )
        result = await self.session.execute(smt)
        actor = result.scalars().all()
        return actor
