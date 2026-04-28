import datetime
import uuid
from pydantic import BaseModel, Field, field_serializer
from typing import List, Optional
from app.scheme.author.model_author import AuthorResponse
from app.scheme.actor.model_actor import ActorResponse
from app.scheme.comment.model_coment import ComentWithUserResponse
from app.scheme.rating.model_ratingfilms import RatingFilmResponse
from app.scheme.country.country_base import CountryShort
from app.scheme.film.type_film import TypeFilmResponse
from app.scheme.film.film_base import (
    FilmBase,
    FilmBaseResponse,
    FilmBaseList,
)
from app.scheme.review.model_review import ReviewInfo


class FilmCreateRequest(FilmBase):
    country_id: Optional[uuid.UUID] = None


class FilmUpdateRequest(BaseModel):
    description: Optional[str] = Field(min_length=10, max_length=10000)
    title: Optional[str] = Field(..., min_length=10, max_length=1000)
    release_date: Optional[datetime.date] = None
    actor_ids: List[uuid.UUID] = []
    author_ids: List[uuid.UUID] = []
    country_id: Optional[uuid.UUID] = None


class FilmResponse(FilmBaseResponse):
    authors: Optional[List[AuthorResponse]] = None
    actors: Optional[List[ActorResponse]] = None
    coments: Optional[List[ComentWithUserResponse]] = []
    rating_films: Optional[List[RatingFilmResponse]] = []
    types_film: Optional[List[TypeFilmResponse]] = []
    reviews: Optional[List[ReviewInfo]] = []
    country: Optional[CountryShort] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None


class FilmResponseBlocFilm(FilmBaseResponse):
    pass


class FilmlListResponse(BaseModel):
    films: List[FilmResponse]


class FilmlListBlockResponse(BaseModel):
    films: List[FilmResponseBlocFilm]


class AddActorFilsmResponse(BaseModel):
    actor_ids: List[uuid.UUID]


class AddAuthorFilsmResponse(BaseModel):
    author_ids: List[uuid.UUID]
