from app.service.base_service import Base_Service
from uuid import UUID
from app.utils.comon import is_name_title 
from litestar.exceptions import HTTPException
from app.list.list_searhc import list_serach_date,list_serach_name_title
class UserService(Base_Service):
    def __init__(self, repo):
        super().__init__(repo)
    async def create_model(self, data, name_title_value=None):
        if not await  is_name_title(model=self.repo.model,session=self.repo.session,name_filed=list_serach_name_title[4],
                                    name_or_title_value=data[list_serach_name_title[4]]):
            raise HTTPException(status_code=409, detail="Пользователь с таким именем уже существует")
        return await super().create_model(data, name_title_value)
    async def update_model(self, model_id, data):
        if not await  is_name_title(model=self.repo.model,session=self.repo.session,name_filed=list_serach_name_title[4]
                                    ,name_or_title_value=data[list_serach_name_title[4]]):
            raise HTTPException(status_code=409, detail="Пользователь с таким именем уже существует")
        return await super().update_model(model_id, data)
    async def get_film_username(self,username:str):
        return await self.repo.get_name(username)
    async def get_password_and_username(self,username:str,password:str):
        return await self.repo.get_username_password(username,password)