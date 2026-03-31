from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class CountryBase(BaseModel):
    country_name: str = Field(min_length=3, max_length=20)


class CountryBaseResponse(BaseModel):
    country_id: UUID
    country_name: Optional[str] = None
    model_config = {"from_attributes": True}


class CountryShort(BaseModel):
    country_name: Optional[str] = None
    model_config = {"from_attributes": True}


class CountryListBaseResponse(BaseModel):
    countrys: List[CountryBaseResponse]
    model_config = {"from_attributes": True}
