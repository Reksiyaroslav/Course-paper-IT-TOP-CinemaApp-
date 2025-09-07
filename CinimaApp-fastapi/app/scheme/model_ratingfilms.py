import datetime

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class RatingFilmCreateRequest(BaseModel):
    rating: int


class RatingFilmUpdateRequest(BaseModel):
    rating: Optional[int] = None


class RatingFilmResponse(BaseModel):
    id: UUID
    rating: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}

class RatingFilmResponseAdmin(BaseModel):
    id:UUID
    film_id:UUID
    user_id:UUID
    rating:Optional[int] =None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}

