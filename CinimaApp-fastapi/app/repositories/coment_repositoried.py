from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model.model_db import Film, User, Coment
from sqlalchemy import select, delete
from app.repositories.repostoried import ModelRepository
from typing import List
import uuid


class ComentRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Coment)

    async def create_coment(self, data, film_id: uuid.UUID, user_id: uuid.UUID):
        coment = Coment(**data, film_id=film_id, user_id=user_id)
        self.session.add(coment)
        await self.session.commit()
        await self.session.refresh(coment)
        return coment

    async def update_like(self, coment_id: uuid.UUID):
        smt = select(Coment).where(Coment.id == coment_id)
        relut = await self.session.execute(smt)
        coment = relut.scalars().one()
        coment.countheart += 1
        await self.session.commit()
        await self.session.refresh(coment)
        return coment

    async def update_unlike(self, coment_id: uuid.UUID):
        smt = select(Coment).where(Coment.id == coment_id)
        relut = await self.session.execute(smt)
        coment = relut.scalars().one()
        coment.countdemon += 1
        await self.session.commit()
        await self.session.refresh(coment)
        return coment
