from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Actor
from sqlalchemy import select, or_,delete



class ActorRepository():
    def __init__(self, session: AsyncSession):
       self.session =session
    async def create_actor(self,data:dict):
        actor = Actor(**data)
        self.session.add(actor)
        await self.session.commit()
        return actor
    async def get_actors(self):
        smt = select(Actor)
        relult = await self.session.execute(smt)
        actor = relult.scalars().all()
        return actor
    async def get_actor_by_id(self,actor_id):
        actor = await self.session.get(Actor,actor_id)
        return actor
    async def update_actor(self,data:dict,actor_id):
        actor = await self.get_actor_by_id(actor_id=actor_id)
        for key,values in data.items():
            if values  is not  None and hasattr(actor,key):
                setattr(actor,key,values)
        await self.session.commit()
        await self.session.refresh(actor)
        return actor
    async def delete_actor(self,actor_id)->dict:
        smt = delete(Actor).filter(Actor.actor_id==actor_id)
        await self.session.execute(smt)
        await self.session.commit()
        return {"message":"Delete actor the db"}
    async def get_actorname(self, actorname: str) -> Actor|None:
        smt = select(Actor).where(
            (Actor.fistname == actorname)
            | (Actor.lastname == actorname)
            | (Actor.patronymic == actorname)
        )
        result = await self.session.execute(smt)
        actor = result.scalars().first()
        return actor

    async def get_actorname_list(self, name: str, limit: int = 3) -> list[Actor]|None:
        serhat_parametr = f"%{name}%"
        smt = (
            select(Actor)
            .where(
                or_(
                    Actor.fistname.contains(serhat_parametr),
                    Actor.lastname.contains(serhat_parametr),
                    Actor.patronymic.contains(serhat_parametr),
                )
            )
            .limit(limit)
        )
        result = await self.session.execute(smt)
        actors = result.scalars().all()
        if not actors:
            return None
        return actors
