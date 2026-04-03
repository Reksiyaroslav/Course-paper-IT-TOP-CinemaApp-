import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.comon import faker, generatao_bio
from app.scheme.film.film_base import FilmShort
from app.scheme.country.country_base import CountryShort


class ScreenWriterBase(BaseModel):
    fistname: str = Field(min_length=3, max_length=50, default_factory=faker.first_name)
    lastname: str = Field(min_length=3, max_length=50, default_factory=faker.last_name)
    birth_date: datetime.date = Field(default_factory=faker.date_of_birth)
    patronymic: str = Field(
        min_length=3, max_length=50, default_factory=faker.first_name
    )
    bio: str = Field(default_factory=generatao_bio)


class ScreenWriterBaseResponse(BaseModel):
    fistname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[datetime.date] = None


class AuthorCreateRequest(ScreenWriterBase):
    country_id: Optional[uuid.UUID] = None


class AuthorUpdateRequest(ScreenWriterBase):
    country_id: Optional[uuid.UUID] = None


class AuthorResponse(ScreenWriterBaseResponse):
    author_id: uuid.UUID
    birth_date: Optional[datetime.date] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class Author_FullResponse(ScreenWriterBaseResponse):
    author_id: uuid.UUID
    birth_date: Optional[datetime.date] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    films_authored: List[Optional[FilmShort]] = []
    country: Optional[CountryShort] = None
    model_config = {"from_attributes": True}


class AuthorlListResponse(BaseModel):
    author: List[AuthorResponse]
