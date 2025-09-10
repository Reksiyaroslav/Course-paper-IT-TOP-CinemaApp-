from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Actor
from sqlalchemy import select, delete,or_
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

    async def get_actorname_list(self, name: str, limit:int=3) -> Actor:
        serhat_parametr = f"%{name}%"
        smt = (
            select(Actor)
            .where(
                or_(
                    Actor.fistname.contains(serhat_parametr),
                    Actor.lastname.contains(serhat_parametr),
                    Actor.patronymic.contains(serhat_parametr)
                )
            )
            .limit(limit)
        )
        result = await self.session.execute(smt)
        actor = result.scalars().all()
        return actor
