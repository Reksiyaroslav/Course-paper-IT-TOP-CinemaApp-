import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional


class ActorCreateRequest(BaseModel):
    fistname: str
    lastname: str
    birth_date: datetime.date
    patronymic: str
    star: int


class ActorUpdateRequest(BaseModel):
    fistname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    star: Optional[int] = None
    birth_date: Optional[datetime.date] = None


class ActorResponse(BaseModel):
    id: uuid.UUID
    fistname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    star: Optional[int] = None
    birth_date: Optional[datetime.date] = None
    create_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class ActorListResponse(BaseModel):
    actors: List[ActorResponse]
