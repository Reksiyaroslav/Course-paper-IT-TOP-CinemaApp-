import datetime
import uuid
from  pydantic import BaseModel
from typing import List,Optional
from uuid import UUID


class RatingFilmCreateRequest(BaseModel):
    rating:int 
    film_id:UUID
    user_id:UUID
    


class RatingFilmUpdateRequest(BaseModel):
    rating:Optional[int] =None 

class RatingFilmResponse(BaseModel):
    id:uuid.UUID
    film_id:Optional[UUID] = None 
    user_id:Optional[UUID]
    rating:Optional[int] =None
    created_at:Optional[datetime.datetime] = None
    update_date:Optional[datetime.datetime] = None
    model_config = {
        "from_attributes": True
    }




