from app.service.base_service import Base_Service
from uuid import UUID
from fastapi.exceptions import HTTPException
from app.list.list_searhc import list_serach_date
from app.utils.comon import (
    is_fistname_lastname,
    validet_star_rating,
    validate_is_data_range,
)


class ActorService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)

    async def create_model(self, data, name_title_value=None):
        if await validate_is_data_range(data[list_serach_date[1]], "actor"):
            if await validet_star_rating(data, "star"):
                if not await is_fistname_lastname(
                    self.repo.model, self.repo.session, data
                ):
                    raise HTTPException(detail="Такой актёр уже есть ", status_code=400)
                return await super().create_model(data, name_title_value)
            raise HTTPException(
                detail="Что не так с оценкой возможно не находится в дипозоне 1 от 10",
                status_code=400,
            )
        raise HTTPException(
            detail="Что не так сдадой рождения возможно не находится дипозоне 2025  или 1945",
            status_code=404,
        )

    async def update_model(self, model_id, data):
        if list_serach_date[1] in data and data[list_serach_date[1]] is not None:
            if await validate_is_data_range(data[list_serach_date[1]], "actor"):
                if "star" in data and data["star"] is not None:
                    if await validet_star_rating(data, "star"):
                        if not await is_fistname_lastname(
                            self.repo.model, self.repo.session, data
                        ):
                            raise HTTPException(
                                detail="Такой актёр уже есть ", status_code=400
                            )

                    raise HTTPException(
                        detail="Что не так с оценкой возможно не находится в дипозоне 1 от 7",
                        status_code=400,
                    )
            raise HTTPException(
                detail="Что не так сдадой рождения возможно не находится дипозоне 2025  или 1945",
                status_code=400,
            )
        return await super().update_model(model_id, data)

    async def get_fistname_lastname_pat(self, name: str):
        if not name or not name.strip():
            raise HTTPException(status_code=424, detail="Нет такой актера часть имени ")
        return await self.repo.get_actorname(name.strip())

    async def get_serahc_name_list(self, name: str):
        if not name or not name.strip():
            raise HTTPException(status_code=424, detail="Нет такой актера часть имени ")
        elif len(name) < 2:
            raise HTTPException(
                status_code=400, detail="Имя актера должно быть не меньше 2 сиволов  "
            )
        return await self.repo.get_actorname(name.strip())
