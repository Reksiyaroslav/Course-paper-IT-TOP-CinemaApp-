from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model_db.model_db  import Film
from sqlalchemy import select,delete,update
from uuid import UUID
from typing import Type,TypeVar,Generic,Optional,List
ModelType = TypeVar("ModelType")
class ModelRepository(Generic[ModelType]):
    def __init__(self,session:AsyncSession,model:Type[ModelType]):
        self.session = session
        self.model = model
    async def create(self,data:dict)->ModelType:
        structure = self.model(**data)

        self.session.add(structure)

        await self.session.commit()
        await self.session.refresh(structure)
        return structure
    async def get_list_model(self)->List[ModelType]:
       
        relutt = await self.session.execute(select(self.model))
        structure = relutt.scalars().all()
        return structure
    async def get_model_id(self,model_id:UUID)->Optional[ModelType]:
        smt = select(self.model).where(self.model.id==model_id)
        relutt = await self.session.execute(smt)
        structure = relutt.scalars().first()
        return structure
    async def update_model(self,model_id:UUID,data:dict)->Optional[ModelType]|None:
        structure = await self.get_model_id(model_id)
        if not structure:
            return None
        for key,value in data.items():
            setattr(structure,key,value)
        await self.session.commit()
        await self.session.refresh(structure)
        return structure
    async def model_delete(self ,model_id:UUID)->bool:
        smt = delete(self.model).where(self.model.id == model_id)
        reluts = await self.session.execute(smt)
        await self.session.commit()
        return reluts.rowcount> 0