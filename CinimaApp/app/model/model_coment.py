import datetime
import uuid
from pydantic import BaseModel
from typing import List, Optional


class ComentCreateRequest(BaseModel):
    description: str
    countheart: int
    countdemon: int
    film_id: uuid.UUID
    user_id: uuid.UUID


class ComentUpdateRequest(BaseModel):
    description: Optional[str] = None
    countheart: Optional[int] = None
    countdemon: Optional[int] = None


class ComentResponse(BaseModel):
    id: uuid.UUID
    description: Optional[str] = None
    countheart: Optional[int] = None
    countdemon: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}
