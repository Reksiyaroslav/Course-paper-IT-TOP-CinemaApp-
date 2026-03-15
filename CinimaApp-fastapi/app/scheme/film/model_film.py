import datetime
import uuid
from pydantic import BaseModel, Field,field_serializer
from typing import List, Optional
from app.scheme.author.model_author import AuthorResponse
from app.scheme.actor.model_actor import ActorResponse
from app.scheme.comment.model_coment import ComentWithUserResponse
from app.scheme.rating.model_ratingfilms import RatingFilmResponse
from app.scheme.film.film_base import FilmBase,FilmBaseResponse
class FilmCreateRequest(FilmBase):
    pass


class FilmUpdateRequest(BaseModel):
    description: Optional[str] = Field(min_length=10, max_length=10000)
    title: Optional[str] = Field(..., min_length=10, max_length=1000)
    release_date: Optional[datetime.date] = None
    actor_ids: List[uuid.UUID] = None
    author_ids: List[uuid.UUID] = None


class FilmResponse(FilmBaseResponse):
    film_id: uuid.UUID
    authors: Optional[List[AuthorResponse]] = None
    actors: Optional[List[ActorResponse]] = None
    coments: Optional[List[ComentWithUserResponse]] = []
    rating_films: Optional[List[RatingFilmResponse]] = []
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    avg_rating: float = 0.0
    path_image: Optional[str] = "images/cat.jpg"
    model_config = {"from_attributes": True}


class FilmResponseBlocFilm(BaseModel):
    film_id: uuid.UUID
    title: Optional[str]
    description: Optional[str]
    path_image: Optional[str] = "images/cat.jpg"
    avg_rating: float   = 0.0
    model_config = {"from_attributes": True}
    @field_serializer('film_id')
    def serialize_film_id(self, value: uuid.UUID) -> str:
        return str(value)


class FilmlListResponse(BaseModel):
    films: List[FilmResponse]
class FilmlListBlockResponse(BaseModel):
    films: List[FilmResponseBlocFilm]

class AddActorFilsmResponse(BaseModel):
    actor_ids: List[uuid.UUID]


class AddAuthorFilsmResponse(BaseModel):
    author_ids: List[uuid.UUID]
