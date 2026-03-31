from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.db.model.model_db import TypeFilm


class TypeFilmReposit:
    def __init__(self, session) -> None:
        self.session: AsyncSession = session

    async def create_type_film(self, data: dict):
        try:
            type_film = TypeFilm(**data)
            self.session.add(type_film)
            await self.session.commit()
            await self.session.refresh(type_film)
            return type_film
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error crete type_film: {str(e)}")

    async def get_types_film(self):
        smt = select(TypeFilm)
        relult = await self.session.execute(smt)
        return relult.scalars().all()

    async def get_type_film_by_id(self, type_film_id: UUID):
        return await self.session.get(TypeFilm, type_film_id)

    async def update_type_film(self, data: dict, type_film_id: UUID):
        try:
            type_film = await self.get_type_film_by_id(type_film_id=type_film_id)
            for key, value in data.items():
                setattr(type_film, key, value)
            await self.session.commit()
            await self.session.refresh(type_film)
            return type_film
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Error update type_film: {str(e)}")

    async def delete_type_film(self, type_film_id: UUID):
        try:
            smt = delete(TypeFilm).where(TypeFilm.type_film_id == type_film_id)
            relult = await self.session.execute(smt)
            await self.session.commit()
            return True
        except Exception:
            print(Exception)
            await self.session.rollback()
            return False
