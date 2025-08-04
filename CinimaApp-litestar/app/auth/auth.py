from litestar.contrib.jwt import JWTAuth
from litestar.params import Dependency
from datetime import datetime,timedelta
import os 
from  typing import Any
from dotenv import load_dotenv
from litestar import post,  get,Request,Controller
from litestar.di import Provide
from litestar.exceptions import HTTPException
from app.repositories.users_repositorie import UserRepository,User
from app.model.model_user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
load_dotenv()
 

JWT_SECRET  = "Hello-mane_or_women"

JWT_ALGORITHM = "HS256"
ACCESSS_TOKEN_MINUTES = 30 
class LogiUser(BaseModel):
    username:str
    password:str
class TokenLog(BaseModel):
    access_token: str
    token_type: str

class MessageProtected(BaseModel):
    message:str
    user:UserResponse

def create_access_tocen(data:dict,expires_delta:timedelta| None =None):
    to_econde = data.copy()
    expire =datetime.utcnow()+(expires_delta or timedelta(minutes=ACCESSS_TOKEN_MINUTES))
    to_econde.update({"exp": int(expire.timestamp())})
    user_id = str(to_econde.get("sub"))
    token =  jwt_auth.create_token(identifier=user_id,token_extras=to_econde)

    return token
async def authehticate_and_get_token(username:str,password:str,user_repo:UserRepository):
    
    user = await user_repo.get_username_password(username,password)
    if not user:
        raise HTTPException(status_code=404,detail="Not user db")
    token = create_access_tocen({"sub":str(user.id),"username":user.username})
    return token
async def retrieve_user_handler(token_paloy:dict,async_session:AsyncSession=Dependency())->UserResponse:
    user_repo = UserRepository(async_session)
    user_id = token_paloy.get("sub")
    if not user_id:
        raise HTTPException(status_code=404,detail="Not user fond user_id")
    user = await user_repo.get_model_id(user_id)
    return UserResponse.from_orm(user)




jwt_auth  = JWTAuth(token_secret=JWT_SECRET,algorithm=JWT_ALGORITHM,retrieve_user_handler=retrieve_user_handler, 
                    exclude=["/schema", "/","login"])


class AuthController(Controller):
    path = "/login"
    security =[]
    tags = ["login"] 
    @post()
    
    async def login(self,data:LogiUser,async_session:AsyncSession=Dependency())->TokenLog:
        username = data.username
        password = data.password
        user_repo = UserRepository(async_session)
        if not username or not password:
            raise HTTPException(status_code=400,detail="Username and password required")
        token = await authehticate_and_get_token(username,password,user_repo)
        return TokenLog(access_token=token,token_type="bearer")
        
class ProtectedController(Controller):
    path = "/protected"
    tags = ["protected"] 
#не рабоатет выдаёт ошибку 
    @get()
    async def protected_router(self,request: Request[UserResponse,dict,Any])->MessageProtected:
        
        return MessageProtected(message="Secret data",user=request.user)
        
