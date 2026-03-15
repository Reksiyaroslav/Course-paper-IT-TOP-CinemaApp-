
import uuid
import datetime
from pydantic import BaseModel, Field
from pydantic import EmailStr
from typing import Optional
from app.scheme._base import BaseSheman
from app.utils.comon import faker
class UserBase(BaseModel):
    username: str = Field(
        ..., min_length=5, max_length=60, default_factory=faker.user_name
    )
    email: EmailStr = Field(default_factory=faker.email)
    password: str = Field(
        ..., min_length=8, max_length=15, default_factory=faker.password
    )
class UserBaseResponse(BaseModel):
    username: Optional[str] =None 
    email: Optional[str] = None
class UserShort(BaseSheman):
    user_id: uuid.UUID
    username: str
    email: str
    created_at: datetime.datetime | None = None
class UserReponseNotInfo(UserBaseResponse):
    user_id: uuid.UUID
    username: str | None = None
    
    model_config = {"from_attributes": True}