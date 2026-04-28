from pydantic import BaseModel, Field
from typing import List
from uuid import UUID


class ReviewBase(BaseModel):
    description: str
    rating_histrory: int = Field(ge=1, le=10)
    rating_musing: int = Field(ge=1, le=10)
    rating_persons: int = Field(ge=1, le=10)
    rating_atmosphere: int = Field(ge=1, le=10)
    is_reviewer: bool = Field(default=False)


class ReviewBaseReponse(BaseModel):
    review_id: UUID
    description: str
    rating_histrory: int
    rating_musing: int
    rating_persons: int
    rating_atmosphere: int
    is_reviewer: bool
    avg_rating: int
    model_config = {"from_attributes": True}


class ReviewBaseList(BaseModel):
    reviews: List[ReviewBaseReponse] = []
    model_config = {"from_attributes": True}
