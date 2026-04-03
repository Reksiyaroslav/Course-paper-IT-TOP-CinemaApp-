import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.comon import faker, generator_star
from app.scheme.film.film_base import FilmShort
from app.scheme.country.country_base import CountryShort


class ActorBase(BaseModel):
    fistname: str = Field(min_length=3, max_length=50, default_factory=faker.first_name)
    lastname: str = Field(min_length=3, max_length=50, default_factory=faker.last_name)
    birth_date: datetime.date = Field(default_factory=faker.date_of_birth)
    patronymic: str = Field(
        min_length=3, max_length=50, default_factory=faker.first_name
    )
    star: int = Field(ge=1, le=10, default_factory=generator_star)


class ActorBaseResponse(BaseModel):
    fistname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    star: Optional[int] = None
    birth_date: Optional[datetime.date] = None


class ActorCreateRequest(ActorBase):
    country_id: Optional[uuid.UUID] = None


class ActorUpdateRequest(ActorBase):
    country_id: Optional[uuid.UUID] = None


class ActorResponse(ActorBaseResponse):
    actor_id: uuid.UUID
    create_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class Actor_FullResponse(ActorBaseResponse):
    actor_id: uuid.UUID
    create_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    films_acted: List[Optional[FilmShort]] = []
    country: Optional[CountryShort] = None
    model_config = {"from_attributes": True}


class ActorListResponse(BaseModel):
    actors: List[ActorResponse]
