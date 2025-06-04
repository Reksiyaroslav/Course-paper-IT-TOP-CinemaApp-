import datetime
import uuid
from  pydantic import BaseModel
from typing import List,Optional
from app.model.model_author import AuthorResponse
from app.model.model_actor import ActorResponse


class FilmCreateRequest(BaseModel):
    description:str 
    title:str
    release_date:datetime.date
    estimation:int 
    


class FilmUpdateRequest(BaseModel):
    description:Optional[str] =None 
    title:Optional[str] =None 
    release_date:Optional[datetime.datetime] = None 
    estimation:Optional[int]  = None 
    actor_ids:List[uuid.UUID]
    author_ids:List[uuid.UUID]

class FilmResponse(BaseModel):
    id:uuid.UUID
    description:Optional[str] =None
    title:Optional[str] = None
    release_date:Optional[datetime.date] =None
    estimation:Optional[int] =None
    authors: List[AuthorResponse]  =None
    actors: List[ActorResponse] = None
    create_date:Optional[datetime.datetime] = None
    model_config = {
        "from_attributes": True
    }


class FilmlListResponse(BaseModel):
    films:List[FilmResponse]

class AddActorFilsmResponse(BaseModel):
    actor_ids:List[uuid.UUID]
class AddAuthorFilsmResponse(BaseModel):
    author_ids:List[uuid.UUID]