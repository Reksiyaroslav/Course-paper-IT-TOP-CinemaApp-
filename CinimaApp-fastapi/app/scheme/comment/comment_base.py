from pydantic import BaseModel, Field
import uuid
import datetime
from app.scheme._base import BaseSheman
class ComenntBase(BaseModel):
    description: str = Field(min_length=20,max_length=4000)
class ComentShort(BaseSheman):
    coment_id: uuid.UUID
    description: str 
    countheart: int = Field(default=0)
    countdemon: int = Field(default=0)
    created_at: datetime.datetime |None = None
    update_at: datetime.datetime |None = None