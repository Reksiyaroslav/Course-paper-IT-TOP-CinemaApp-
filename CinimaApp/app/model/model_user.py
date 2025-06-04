from pydantic import BaseModel,Field
from typing import Optional
import uuid
import datetime


class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    datetimenow:datetime.datetime 

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    datetimenow:Optional[datetime.datetime] = None
    update_date:Optional[datetime.datetime] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password: str
    datetimenow:Optional[datetime.datetime]  =  Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
    created_at: datetime.datetime = None
    update_date:Optional[datetime.datetime] = None
    model_config = {
        "from_attributes": True
    }