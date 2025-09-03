import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.comon import generatao_destripsion


class ComentCreateRequest(BaseModel):
    description: str = Field(default_factory=generatao_destripsion)


class ComentUpdateRequest(BaseModel):
    description: Optional[str] = None


class ComentResponse(BaseModel):
    id: uuid.UUID
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
