from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class TypeFilmBase(BaseModel):
    type_film_name: str = Field(min_length=5, max_length=40)


class TypeFilmCreateRequest(TypeFilmBase):
    pass


class TypeFilmUpdateRequest(TypeFilmBase):
    pass


class TypeFilmResponse(BaseModel):
    type_film_id: UUID
    type_film_name: Optional[str] = None
    model_config = {"from_attributes": True}


class ListTypeFilmResponse(BaseModel):
    types_film: List[TypeFilmResponse]
    model_config = {"from_attributes": True}
