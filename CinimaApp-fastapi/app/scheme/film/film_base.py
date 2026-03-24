from pydantic import BaseModel, Field
import uuid
import datetime
from app.scheme._base import BaseSheman
from typing import Optional


class FilmBase(BaseModel):
    description: str = Field(min_length=10, max_length=10000)
    title: str = Field(..., min_length=10, max_length=1000)
    release_date: datetime.date


class FilmShort(BaseSheman):
    film_id: uuid.UUID
    title: str
    description: str | None = None
    release_date: datetime.date | None = None
    path_image: str | None = "images/cat.jpg"
    avg_rating: float = 0.0


class FilmBaseResponse(BaseModel):
    description: Optional[str] = None
    title: Optional[str] = None
    release_date: Optional[datetime.date] = None
