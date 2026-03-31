from fastapi.exceptions import HTTPException
from uuid import UUID

from app.scheme.country.model_country import (
    CountryBaseResponse,
    CountryListBaseResponse,
)
from app.repositories.country_reposutorie import CountryRepossitoried
from app.service.base_service import Base_Service
from app.utils.noramliz_text import normalize_data

from app.enums.type_model import TypeModel


class CountryService(Base_Service):
    def __init__(self, session):
        super().__init__(session)
        self.country_repo: CountryRepossitoried = CountryRepossitoried(self.session)

    async def create_country(self, data: dict):
        try:
            clean_data = normalize_data(data=data, model_type=TypeModel.Country.value)
            new_contry = await self.country_repo.create_country(data=clean_data)
            return CountryBaseResponse.from_orm(new_contry)
        except HTTPException:
            raise HTTPException(status_code=500, detail="Ошибка при создании  страны")

    async def get_countrys(self):
        countrys = await self.country_repo.get_countrys()
        return CountryListBaseResponse(countrys=countrys)

    async def get_country_by_id(self, country_id):
        country = await self.country_repo.get_country_by_id(country_id)
        if not country:
            raise HTTPException(
                detail="Нет страны  с таким id",
                status_code=404,
            )
        return CountryBaseResponse.from_orm(country)

    async def update_country(self, data, country_id):
        update_type_film = await self.country_repo.update_country(
            data=data, country_id=country_id
        )
        return CountryBaseResponse.from_orm(update_type_film)

    async def delete_country(self, country_id):
        await self.country_repo.delete_country(country_id=country_id)
        return {"detail": "Удалили страны "}
