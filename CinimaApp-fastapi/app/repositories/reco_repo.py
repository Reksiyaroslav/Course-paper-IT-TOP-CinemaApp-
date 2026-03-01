from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from uuid import UUID
from app.db.model.model_db import Recone, Type_Rec


class RecoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_reco(self, user_id: UUID, type_rec: str, coment_id: UUID):
        reco: Recone = Recone(
            repit_user_id=user_id, coment_recone=coment_id, type_rect=type_rec
        )
        self.session.add(reco)
        await self.session.commit()
        return "Create Rect"

    async def get_recos(self) -> list[Recone]:
        smt = select(Recone)
        relulst = await self.session.execute(smt)
        return relulst.scalars().all()

    async def get_reco_user_id_coment_id(self, user_id, coment_id):
        smt = select(Recone).where(
            Recone.repit_user_id == user_id and Recone.coment_recone == coment_id
        )
        relult = await self.session.execute(smt)
        reco = relult.scalars().first()
        return reco

    async def update_reco(self, user_id: UUID, type_rec: str, coment_id: UUID):
        smt = select(Recone).where(
            Recone.repit_user_id == user_id, Recone.coment_recone == coment_id
        )
        relult = await self.session.execute(smt)
        reco = relult.scalars().one()
        if reco.type_rect != type_rec:
            reco.type_rect = type_rec
        await self.session.commit()
        await self.session.refresh(reco)
        return reco

    async def delete_reco(self, user_id, coment_id):
        smt = delete(Recone).where(
            Recone.repit_user_id == user_id, Recone.coment_recone == coment_id
        )
        await self.session.execute(smt)
        await self.session.commit()
        return None
