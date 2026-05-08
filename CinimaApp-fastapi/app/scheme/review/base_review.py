from pydantic import BaseModel, Field
from typing import List,Optional
from uuid import UUID
from datetime import datetime

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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


class ReviewBaseList(BaseModel):
    reviews: List[ReviewBaseReponse] = []
    model_config = {"from_attributes": True}
