from uuid import UUID
from fastapi.exceptions import HTTPException
from app.service.base_service import Base_Service
from app.repositories.coment_repositoried import ComentRepository, Type_Rec
from app.repositories.reco_repo import RecoRepository

from app.utils.comon import validet_text_coment


class ComentService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.coment_repo: ComentRepository = ComentRepository(self.session)
        self.reco_repo: RecoRepository = RecoRepository(self.session)

    async def create_model(
        self,
        data,
        film_id: UUID,
        user_id: UUID,
        name_title_value=None,
    ):
        if not await validet_text_coment(data, "description"):
            raise HTTPException(
                detail="Использовали не нужное слова в тексте", status_code=404
            )

        return await self.coment_repo.create_coment(data, film_id, user_id)

    async def get_coments(self):
        return await self.coment_repo.get_coments()

    async def get_by_id_coment(self, coment_id):
        return await self.coment_repo.get_by_id_coments(coment_id)

    async def update_coment(self, coment_id, data):
        if not await validet_text_coment(data, "description"):
            raise HTTPException(
                detail="Использовали не нужное слова в тексте", status_code=404
            )
        return await self.coment_repo.update_coment(coment_id=coment_id, data=data)

    async def delete_coment(self, coment_id):
        return await self.coment_repo.delete_coment(coment_id=coment_id)

    async def update_comet_like_unlike(self, user_id: UUID, coment_id, type_rec: str):
        if type_rec not in (Type_Rec.Like.value, Type_Rec.UnLike.value):
            raise HTTPException(
                detail="Вы не можете передавть сюда только unlike like больше не чего ",
                status_code=400,
            )
        old_reco = await self.reco_repo.get_reco_user_id_coment_id(user_id, coment_id)
        old_type = old_reco.type_rect if old_reco else None
        if old_reco is None:
            await self.reco_repo.create_reco(
                user_id=user_id, coment_id=coment_id, type_rec=type_rec
            )
        elif old_type == type_rec:
            if old_reco:
                await self.reco_repo.delete_reco(user_id=user_id, coment_id=coment_id)
        else:
            await self.reco_repo.update_reco(
                user_id=user_id, coment_id=coment_id, type_rec=type_rec
            )
        return await self.coment_repo.update_type_recon(
            coment_id=coment_id, type_recon=type_rec, relult_recon=old_type
        )

    async def list_user_coments(self, user_id: UUID):
        return await self.coment_repo.list_user_coments(user_id)

    async def list_film_coments(self, film_id: UUID):
        return await self.coment_repo.list_film_coments(film_id)
