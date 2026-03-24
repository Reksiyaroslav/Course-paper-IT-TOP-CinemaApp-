import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class RatingFilmBase(BaseModel):
    rating: int = Field(ge=1, le=10, description="Number rating")


class RatingFilmBaseResponse(BaseModel):
    rating: Optional[int] = None


class RatingFilmCreateRequest(RatingFilmBase):
    pass


class RatingFilmUpdateRequest(RatingFilmBase):
    pass


class RatingFilmResponse(RatingFilmBaseResponse):
    rating_id: UUID
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class RatingFilmResponseAdmin(RatingFilmBaseResponse):
    rating_id: UUID
    film_id: UUID
    user_id: UUID
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class RatingFilmList(BaseModel):
    rating_list: List[RatingFilmResponse]


class RatingFilmListAdmin(BaseModel):
    rating_list: List[RatingFilmResponseAdmin]


RatingFilmResponse.model_rebuild()
