from __future__ import annotations
from pydantic import BaseModel, Field
from pydantic import EmailStr
from typing import Optional, List
import uuid
import datetime
from app.scheme.comment.model_coment import ComentResponse
from app.scheme.film.model_film import FilmResponseBlocFilm,RatingFilmResponse
from app.scheme.user.user_base import  UserBase,UserBaseResponse,faker
class UserCreateRequest(UserBase):
  pass

class UserLogin(BaseModel):
    email:EmailStr
    password:str
class UserUpdateRequest(BaseModel):
    username: Optional[str] = Field(
        ..., min_length=5, max_length=60, default_factory=faker.user_name
    )
    email: Optional[EmailStr] = Field(default_factory=faker.email)
    password: Optional[str]  = Field(
        ..., min_length=8, max_length=15, default_factory=faker.password
    )
class UserResponse(UserBaseResponse):
    user_id: uuid.UUID
    datetimenow: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    coments: List['ComentResponse'] = []
    ratings: List['RatingFilmResponse'] = []
    likefilms: List['FilmResponseBlocFilm'] = []
    # friends: List[UserResponseFrends]=[]
    model_config = {"from_attributes": True}


# class UserResponseFrends(BaseModel):
# friends: List[UserResponse]=[]

class UserRensponseAdmin(UserBaseResponse):
    user_id: uuid.UUID
    coments: List['ComentResponse'] = []
    ratings: List['RatingFilmResponse'] = []
    likefilms: List['FilmResponseBlocFilm'] = []
    # friends: List[UserResponseFrends]=[]
    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
   user_list:List[UserResponse]
   model_config = {"from_attributes": True}
class UserListAdminResponse(BaseModel):
   user_admin_list:List[UserRensponseAdmin]
class AddFilmUserResponse(BaseModel):
    film_id: uuid.UUID
