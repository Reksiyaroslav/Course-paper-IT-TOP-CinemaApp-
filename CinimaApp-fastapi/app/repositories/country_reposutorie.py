from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List
from app.db.model.model_db import Country


class CountryRepossitoried:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create_country(self, data: dict):
        try:
            new_country = Country(**data)
            self.session.add(new_country)
            await self.session.commit()
            await self.session.refresh(new_country)
            return new_country
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(Exception(f"Error сreate country: {str(e)}"))
            return None

    async def get_countrys(self):
        smt = select(Country)
        relult = await self.session.execute(smt)
        return relult.scalars().all()

    async def get_country_by_id(self, country_id: UUID):
        return await self.session.get(Country, country_id)

    async def update_country(self, country_id: UUID, data: dict):
        try:
            country = await self.get_country_by_id(country_id=country_id)
            for key, value in data.items():
                setattr(country, key, value)
            await self.session.commit()
            await self.session.refresh(country)
            return country
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error update country: {str(e)}")

    async def delete_country(self, country_id: UUID):
        try:
            smt = delete(Country).where(Country.country_id == country_id)
            relult = await self.session.execute(smt)
            await self.session.commit()
            return True
        except Exception:
            print(Exception)
            await self.session.rollback()
            return False

    async def update_country_not_double(self, country_id: UUID, name_country: str):
        clean_name = name_country.strip().lower()
        smt = select(Country).where(
            and_(
                Country.country_id != country_id,
                func.lower(Country.country_name) == clean_name,
            )
        )
        relult = await self.session.execute(smt)
        return relult.scalars().first() is not None

    async def is_country_not_double(self, name_country: str):
        clean_name = name_country.strip().lower()
        smt = select(Country).where(func.lower(Country.country_name) == clean_name)
        relult = await self.session.execute(smt)
        return relult.scalars().first() is not None
