from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, inspect
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from typing import Type, TypeVar, Generic, Optional, List
import logging

ModelType = TypeVar("ModelType")


class ModelRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, data: dict) -> ModelType:
        try:
            structure = self.model(**data)
            self.session.add(structure)
            await self.session.commit()
            await self.session.refresh(structure)
            return structure
        except SQLAlchemyError as e:
            logging.error(f"Error creating model: {e}")
            await self.session.rollback()
            return None

    async def get_list_model(self) -> List[ModelType]:
        try:
            relutt = await self.session.execute(select(self.model))
            structure = relutt.scalars().all()
            return structure
        except SQLAlchemyError as e:
            logging.error(f"Error creating model: {e}")
            await self.session.rollback()
            return None

    async def get_model_id(self, model_id: UUID) -> Optional[ModelType]:
        try:
            smt = select(self.model).where(self.model.id == model_id)
            relutt = await self.session.execute(smt)
            structure = relutt.scalars().first()
            return structure
        except SQLAlchemyError as e:
            logging.error(f"Error creating model: {e}")
            await self.session.rollback()
            return None

    async def update_model(self, model_id: UUID, data: dict) -> Optional[ModelType]:
        try:
            structure = await self.get_model_id(model_id)
            if not structure:
                return None
            for key, value in data.items():
                if value is not None:
                    setattr(structure, key, value)

            await self.session.commit()
            await self.session.refresh(structure)
            return structure
        except SQLAlchemyError as e:
            logging.error(f"Error creating model: {e}")
            await self.session.rollback()
            raise

    async def model_delete(self, model_id: UUID) -> bool:
        try:
            smt = delete(self.model).where(self.model.id == model_id)
            reluts = await self.session.execute(smt)
            await self.session.commit()
            return reluts.rowcount > 0
        except SQLAlchemyError as e:
            logging.error(f"Error creating model: {e}")
            await self.session.rollback()
            return None
