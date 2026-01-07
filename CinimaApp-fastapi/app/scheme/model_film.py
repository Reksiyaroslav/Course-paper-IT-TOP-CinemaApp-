import datetime
import uuid
from pydantic import BaseModel,Field
from typing import List, Optional
from app.scheme.model_author import AuthorResponse
from app.scheme.model_actor import ActorResponse
from app.scheme.model_coment import ComentResponse
from app.scheme.model_ratingfilms import RatingFilmResponse


class FilmCreateRequest(BaseModel):
    description: str= Field(min_length=10,max_length=10000)
    title: str = Field(...,mmin_length=10,max_length=1000)
    release_date: datetime.date


class FilmUpdateRequest(BaseModel):
    description: Optional[str] = Field(min_length=10,max_length=1000)
    title: Optional[str] = Field(min_length=10,max_length=10000)
    release_date: Optional[datetime.date] = None
    actor_ids: List[uuid.UUID] = None
    author_ids: List[uuid.UUID] = None
    path_images: Optional[str] = None


class FilmResponse(BaseModel):
    film_id: uuid.UUID
    description: Optional[str] = None
    title: Optional[str] = None
    release_date: Optional[datetime.date] = None
    authors: Optional[List[AuthorResponse]] = None
    actors: Optional[List[ActorResponse]] = None
    coments: Optional[List[ComentResponse]] = []
    rating_films: Optional[List[RatingFilmResponse]] = []
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    avg_rating:float = 0.0
    path_image: Optional[str] = "../images/cat.jpg"
    model_config = {"from_attributes": True}
class FilmResponseBlocFilm(BaseModel):
    film_id:uuid.UUID
    title:Optional[str] 
    description:Optional[str]
    path_image: Optional[str] = "../images/cat.jpg"
    avg_rating: float 
    model_config = {"from_attributes": True}

class FilmlListResponse(BaseModel):
    films: List[FilmResponse]


class AddActorFilsmResponse(BaseModel):
    actor_ids: List[uuid.UUID]


class AddAuthorFilsmResponse(BaseModel):
    author_ids: List[uuid.UUID]
