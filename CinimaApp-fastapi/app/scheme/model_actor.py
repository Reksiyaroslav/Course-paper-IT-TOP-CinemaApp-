import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.comon import faker, generator_star


class ActorCreateRequest(BaseModel):
    fistname: str = Field(default_factory=faker.first_name)
    lastname: str = Field(default_factory=faker.last_name)
    birth_date: datetime.date = Field(default_factory=faker.date_of_birth)
    patronymic: str = Field(default_factory=faker.first_name)
    star: int = Field(default_factory=generator_star)


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
