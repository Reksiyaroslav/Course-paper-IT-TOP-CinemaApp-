import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.comon import faker, generatao_bio


class AuthorCreateRequest(BaseModel):
    fistname: str = Field(default_factory=faker.first_name)
    lastname: str = Field(default_factory=faker.last_name)
    birth_date: datetime.date = Field(default_factory=faker.date_of_birth)
    patronymic: str = Field(default_factory=faker.first_name)
    bio: str = Field(default_factory=generatao_bio)


class AuthorUpdateRequest(BaseModel):
    fistname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[datetime.date] = None


class AuthorResponse(BaseModel):
    id: uuid.UUID
    fistname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[datetime.date] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class AuthorlListResponse(BaseModel):
    author: List[AuthorResponse]
