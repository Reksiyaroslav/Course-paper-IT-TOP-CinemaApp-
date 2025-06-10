import datetime
import uuid
from  pydantic import BaseModel
from typing import List,Optional
from app.model.model_author import AuthorResponse
from app.model.model_actor import ActorResponse
from app.model.model_coment import ComentResponse
from app.model.model_ratingfilms import RatingFilmResponse
class FilmCreateRequest(BaseModel):
    description:str 
    title:str
    release_date:datetime.date
    estimation:int


class FilmUpdateRequest(BaseModel):
    description:Optional[str] =None 
    title:Optional[str] =None 
    estimation:Optional[int] = None
    release_date:Optional[datetime.date] = None 
    actor_ids:List[uuid.UUID] =None
    author_ids:List[uuid.UUID]=None
    coment_ids:List[uuid.UUID]=None

class FilmResponse(BaseModel):
    id:uuid.UUID
    description:Optional[str] =None
    title:Optional[str] = None
    release_date:Optional[datetime.date] =None
    estimation:Optional[int] = 1
    authors: List[AuthorResponse]  =None
    actors: List[ActorResponse] = None
    coments: List[ComentResponse]= []
    ratings:List[RatingFilmResponse] = []
    created_at:Optional[datetime.datetime] = None
    update_at:Optional[datetime.datetime] = None
    model_config = {
        "from_attributes": True
    }


class FilmlListResponse(BaseModel):
    films:List[FilmResponse]

class AddActorFilsmResponse(BaseModel):
    actor_ids:List[uuid.UUID]
class AddAuthorFilsmResponse(BaseModel):
    author_ids:List[uuid.UUID]