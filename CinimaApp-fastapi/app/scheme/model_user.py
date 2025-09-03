from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import datetime
from app.scheme.model_coment import ComentResponse
from app.scheme.model_ratingfilms import RatingFilmResponse
from app.scheme.model_film import FilmResponse
from app.utils.comon import faker


class UserCreateRequest(BaseModel):
    username: str = Field(default_factory=faker.user_name)
    email: str = Field(default_factory=faker.email)
    password: str = Field(default_factory=faker.password)


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    coment_ids: List[uuid.UUID] = None


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    datetimenow: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    coments: List[ComentResponse] = []
    ratings: List[RatingFilmResponse] = []
    likefilms: List[FilmResponse] = []
    # friends: List[UserResponseFrends]=[]
    model_config = {"from_attributes": True}


# class UserResponseFrends(BaseModel):
# friends: List[UserResponse]=[]


class AddFilmUserResponse(BaseModel):
    film_id: uuid.UUID
