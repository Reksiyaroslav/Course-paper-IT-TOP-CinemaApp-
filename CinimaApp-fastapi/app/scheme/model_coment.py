import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional


class ComentCreateRequest(BaseModel):
    description: str


class ComentUpdateRequest(BaseModel):
    description: Optional[str] = None


class ComentResponse(BaseModel):
    coment_id: uuid.UUID
    description: Optional[str] = None
    countheart: Optional[int] = Field(default_factory=0)
    countdemon: Optional[int] = Field(default_factory=0)
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class ComentsListFilmIds(BaseModel):
    film_ids: List[uuid.UUID]


class ComentsListUserIds(BaseModel):
    user_ids: List[uuid.UUID]
