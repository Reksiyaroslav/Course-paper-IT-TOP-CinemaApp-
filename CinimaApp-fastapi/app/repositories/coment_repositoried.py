from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid

from app.db.model.model_db import Coment
from app.utils.enums import Type_Rec


class ComentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_coment(self, data, film_id: uuid.UUID, user_id: uuid.UUID):
        coment = Coment(**data, film_id=film_id, user_id=user_id)
        self.session.add(coment)
        await self.session.commit()
        await self.session.refresh(coment)
        return coment

    async def get_coments(self):
        smt = select(Coment)
        relult = await self.session.execute(smt)
        coments = relult.scalars().all()
        return coments

    async def get_by_id_coments(self, coment_id):
        coment = await self.session.get(Coment, coment_id)
        return coment

    async def update_coment(self, data: dict, coment_id):
        coment = await self.get_by_id_coments(coment_id=coment_id)
        for key, values in data.items():
            if values is not None and hasattr(coment, key):
                setattr(coment, key, values)
        await self.session.commit()
        await self.session.refresh(coment)
        return coment

    async def delete_coment(self, coment_id):  # -> Any:
        smt = delete(Coment).where(Coment.coment_id == coment_id)
        await self.session.execute(smt)
        await self.session.commit()
        return {"message": "Delete coment the db"}

    async def update_type_recon(
        self, coment_id: uuid.UUID, type_recon: str, relult_recon: str = None
    ):
        coment: Coment = await self.get_by_id_coments(coment_id)
        if relult_recon == Type_Rec.Like.value:
            coment.countheart = max(0, coment.countheart - 1)
        elif relult_recon == Type_Rec.UnLike.value:
            coment.countdemon = max(0, coment.countdemon - 1)

        if type_recon == Type_Rec.Like.value and relult_recon != Type_Rec.Like.value:
            coment.countheart += 1
        elif (
            type_recon == Type_Rec.UnLike.value
            and relult_recon != Type_Rec.UnLike.value
        ):
            coment.countdemon += 1

        await self.session.commit()
        await self.session.refresh(coment)
        return coment
