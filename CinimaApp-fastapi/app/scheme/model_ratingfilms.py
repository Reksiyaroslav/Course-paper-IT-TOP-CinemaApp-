import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class RatingFilmCreateRequest(BaseModel):
    rating: int = Field(gt=1, lt=10, description="Number rating")


class RatingFilmUpdateRequest(BaseModel):
    rating: Optional[int] = Field(gt=1, lt=10, description="Number rating")


class RatingFilmResponse(BaseModel):
    rating_id: UUID
    rating: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class RatingFilmResponseAdmin(BaseModel):
    rating_id: UUID
    film_id: UUID
    user_id: UUID
    rating: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}
