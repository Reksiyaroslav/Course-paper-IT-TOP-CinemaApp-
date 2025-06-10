from app.utils.comon import is_name_title
from uuid import UUID
class Base_Service:
    def __init__(self,repo):
        self.repo = repo 
    async def create_model(self,data:dict,name_title_value= None):
        return await self.repo.create(data)
    async def get_models(self):
        return await self.repo.get_list_model()
    async def get_model(self,model_id:UUID):
        return await self.repo.get_model_id(model_id)
    async def update_model(self,model_id:UUID,data:dict):
        return await self.repo.update_model(model_id,data)
    async def delete_model(self,model_id:UUID):
        return await self.repo.model_delete(model_id)
