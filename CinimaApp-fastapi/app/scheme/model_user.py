from __future__ import annotations
from pydantic import BaseModel, Field
from pydantic import EmailStr
from typing import Optional, List
import uuid
import datetime
from app.scheme.model_coment import ComentResponse
from app.scheme.model_ratingfilms import RatingFilmResponse
from app.scheme.model_film import FilmResponseBlocFilm
from app.utils.comon import faker


class UserCreateRequest(BaseModel):
    username: str = Field(
        ..., min_length=5, max_length=60, default_factory=faker.user_name
    )
    email: EmailStr = Field(default_factory=faker.email)
    password: str = Field(
        ..., min_length=9, max_length=15, default_factory=faker.password
    )


class UserUpdateRequest(BaseModel):
    username: Optional[str] = Field(min_length=5, max_length=60)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(min_length=9, max_length=15)


class UserResponse(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str
    datetimenow: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    coments: List[ComentResponse] = []
    ratings: List[RatingFilmResponse] = []
    likefilms: List[FilmResponseBlocFilm] = []
    # friends: List[UserResponseFrends]=[]
    model_config = {"from_attributes": True}


# class UserResponseFrends(BaseModel):
# friends: List[UserResponse]=[]


class UserRensponseAdmin(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str
    password: str
    coments: List[ComentResponse] = []
    ratings: List[RatingFilmResponse] = []
    likefilms: List[FilmResponseBlocFilm] = []
    # friends: List[UserResponseFrends]=[]
    model_config = {"from_attributes": True}


class AddFilmUserResponse(BaseModel):
    film_id: uuid.UUID
