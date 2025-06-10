from pydantic import BaseModel,Field
from typing import Optional,List
import uuid
import datetime
from app.model.model_coment import ComentResponse
from app.model.model_ratingfilms import RatingFilmResponse
class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    coment_ids:List[uuid.UUID] =None

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    datetimenow:Optional[datetime.datetime]  =  Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
    created_at: datetime.datetime = None
    update_at:Optional[datetime.datetime] = None
    coments: List[ComentResponse]= []
    ratings:List[RatingFilmResponse] = []
    model_config = {
        "from_attributes": True
    }