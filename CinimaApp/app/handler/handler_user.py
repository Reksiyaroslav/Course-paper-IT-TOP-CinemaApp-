from litestar import get ,post,Controller,delete,put,Request
from litestar.params import Body, Dependency
from app.model.model_user import UserCreateRequest,UserResponse,UserUpdateRequest 
from app.repositories.users_repositorie import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from litestar.exceptions import HTTPException



class UserControlle(Controller):
    path ="/user"
    tags =["User"]
    @post()
    async def create_user(self,data:UserCreateRequest,async_session:AsyncSession=Dependency())->UserResponse:
        user_repo   = UserRepository(async_session) 
        user = await user_repo.create(data.dict())
        return UserResponse.from_orm(user)
    @get()
    async def get_users(self, async_session: AsyncSession = Dependency()) -> list[UserResponse]:
        user_repo = UserRepository(async_session)
        users = await user_repo.get_list_model()
        return [UserResponse.from_orm(user) for user in users]
    @get("/id/{user_id:uuid}")
    async def get_user_id(self,user_id:UUID,async_session:AsyncSession=Dependency())->UserResponse:
        user_repo   = UserRepository(async_session)
        user = await user_repo.get_model_id(user_id)
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)
    @get("/name/{user_name:str}")
    async def get_user_name(self,user_name:str,async_session:AsyncSession=Dependency())->UserResponse:
        user_repo   = UserRepository(async_session)
        user = await user_repo.get_name(user_name)
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)
    @get("/name/{user_name:str}/password/{password:str}")
    async def get_password_username(self,user_name:str,password:str,async_session:AsyncSession=Dependency())->UserResponse:
        user_repo   = UserRepository(async_session)
        user = await user_repo.get_username_password(user_name,password)
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)
    @put("/id/{user_id:uuid}" ,summary="Update user")
    async def update_user(self,user_id:UUID, data:UserUpdateRequest ,async_session:AsyncSession=Dependency())->UserResponse:
        user_repo   = UserRepository(async_session)
        user = await user_repo.update_model(user_id,data.dict(exclude_unset=True))
        if not user:
            raise HTTPException(status_code=404,detail="Not user")
        return UserResponse.from_orm(user)




    
    