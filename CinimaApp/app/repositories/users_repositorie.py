from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.model_db.model_db import User,Coment,RatingFilm
from uuid import UUID
from app.repositories.repostoried import ModelRepository
import bcrypt

class UserRepository(ModelRepository):
    def __init__(self, session: AsyncSession):
       super().__init__(session,model=User)

   
    async def create(self, data):
        if "password"in data:
            password_byte  = data["password"].encode("utf-8")
            salf = bcrypt.gensalt()
            hash = bcrypt.hashpw(password_byte,salf)
            data["password"] = hash.decode("utf-8")
        return await super().create(data)
    
    async def update_model(self, model_id, data):
        if "password"in data and data["password"]!=None:
            password_byte  = data["password"].encode("utf-8")
            salf = bcrypt.gensalt()
            hash = bcrypt.hashpw(password_byte,salf)
            data["password"] = hash.decode("utf-8")
        return await super().update_model(model_id, data)
    
    async def get_name(self,username:str)->User:
        smt = select(User).where(User.username== username)
        result =  await self.session.execute(smt)
        user = result.scalars().first()
        return user
    
    async def get_username_password(self,username:str,password:str)->User:
        
        smt = select(User).where(User.username==username)
        result =  await self.session.execute(smt)
        user = result.scalars().first()
        if not user:
            return None 
        password_hath_user = user.password.encode("utf-8")
        password_send_hath = password.encode("utf-8")
        if bcrypt.checkpw(password_send_hath,password_hath_user):
            return user
        return None
    async def add_coment_user(self,user_id:UUID,coment:Coment):
        user = await self.get_model_id(user_id)
        if user:
            user.coment_users.append(coment)
            await self.session.commit()
            await self.session.refresh(user)
    async def add_ratingfilm_user(self,user_id:UUID,ratingfilm:RatingFilm):
        user = await self.get_model_id(user_id)
        if user:
            user.rating_users.append(ratingfilm)
            await self.session.commit()
            await self.session.refresh(user)