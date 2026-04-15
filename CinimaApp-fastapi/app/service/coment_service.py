from uuid import UUID
from fastapi.exceptions import HTTPException
from app.service.base_service import Base_Service
from app.repositories.coment_repositoried import ComentRepository, Type_Rec
from app.repositories.reco_repo import RecoRepository

from app.utils.comon import validet_text_coment, len_fields

from app.enums.serach_fileld import SerachFiled
from app.enums.type_model import TypeModel
from app.utils.noramliz_text import normalize_data

from app.scheme.comment.model_coment import ComentResponse, ComentListReponse


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
        filed_des = SerachFiled.Des.value[0]

        clean_data = normalize_data(data, TypeModel.Comment.value)
        for key, value in data.items():
            len_fields(value, key)
        if not await validet_text_coment(data, filed_des):
            raise HTTPException(
                detail="Использовали не нужное слова в тексте", status_code=404
            )
        new_comment = await self.coment_repo.create_coment(clean_data, film_id, user_id)
        if not new_comment:
            raise HTTPException(
                status_code=500, detail="Ошибка при создании комментария"
            )
        return ComentResponse.from_orm(new_comment)

    async def get_coments(self):
        comments = await self.coment_repo.get_coments()
        return ComentListReponse(comments=comments)

    async def get_by_id_coment(self, coment_id):
        comment = await self.coment_repo.get_by_id_coments(coment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Комментарий не найден")
        return ComentResponse.from_orm(comment)

    async def update_coment(self, coment_id, data):
        filed_des = SerachFiled.Des.value[0]
        clean_data = normalize_data(data, TypeModel.Comment.value)
        for key, value in data.items():
            len_fields(value, key)
        if not await validet_text_coment(data, filed_des):
            raise HTTPException(
                detail="Использовали не нужное слова в тексте", status_code=404
            )
        update_comment = await self.coment_repo.update_coment(
            coment_id=coment_id, data=clean_data
        )
        if not update_comment:
            raise HTTPException(status_code=404, detail="Комментарий не найден")
        return ComentResponse.from_orm(update_comment)

    async def delete_coment(self, coment_id):
        success = await self.coment_repo.delete_coment(coment_id)
        if not success:
            raise HTTPException(status_code=404, detail="Комментарий не найден")
        return {"message": "Комментарий успешно удалён"}

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
        comment = await self.coment_repo.update_type_recon(
            coment_id=coment_id, type_recon=type_rec, relult_recon=old_type
        )
        if not comment:
            raise HTTPException(status_code=404, detail="Комментарий не найден")
        return ComentResponse.from_orm(comment)
