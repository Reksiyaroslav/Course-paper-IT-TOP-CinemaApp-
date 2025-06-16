from litestar import get ,post,Controller,delete,put,Request
from litestar.params import Body, Dependency
from app.model.model_user import UserCreateRequest,UserResponse,UserUpdateRequest 
from app.repositories.users_repositorie import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from litestar.exceptions import HTTPException
from app.service.user_service import UserService
from app.service.factory import get_service
class UserControlle(Controller):
    path ="/user"
    tags =["User"]
    @post()
    async def create_user(self,async_session:AsyncSession,data:UserCreateRequest)->UserResponse:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        user = await user_service.create_model(data.dict())
        return UserResponse.from_orm(user)
    @get()
    async def get_users(self, async_session: AsyncSession) -> list[UserResponse]:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        users = await user_service.get_models()
        return [UserResponse.from_orm(user) for user in users]
    @get("/id/{user_id:uuid}")
    async def get_user_id(self,user_id:UUID,async_session:AsyncSession)->UserResponse:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        user = await user_service.get_model(user_id)
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)
    """""
    @post("/{user_id:uuid}/friend/{friend_id:uuid}")
    async def add_friend(self,user_id:UUID,friend_id:UUID,async_session:AsyncSession)->UserRepository:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        user = await user_service.add_friend(user_id,friend_id)
        if not user:
            raise HTTPException(status_code=404,detail="Пользователь есть уде друзьях")
        return user 
    """""
    @post("/{user_id:uuid}/film/{likefilm_id:uuid}")
    async def add_likefilm(self,user_id:UUID,likefilm_id:UUID,async_session:AsyncSession)->UserRepository:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        user = await user_service.add_film(user_id,likefilm_id)
        if not user: 
            raise HTTPException(status_code=404,detail="Пользователь есть уде друзьях")
        return UserResponse.from_orm(user) 
    @get("/name/{user_name:str}")
    async def get_user_name(self,user_name:str,async_session:AsyncSession)->UserResponse:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        user = await user_service.get_film_username(user_name)
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)
    @get("/name/{user_name:str}/password/{password:str}")
    async def get_password_username(self,user_name:str,password:str,async_session:AsyncSession)->UserResponse:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        user = await user_service.get_password_and_username(user_name,password)
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)
    @put("/id/{user_id:uuid}" ,summary="Update user")
    async def update_user(self,user_id:UUID, data:UserUpdateRequest ,async_session:AsyncSession)->UserResponse:
        user_service   = get_service(UserService,UserRepository,async_session=async_session) 
        user = await user_service.update_model(user_id,data.dict())
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)




    
    