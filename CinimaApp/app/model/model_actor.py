import datetime
import uuid
from  pydantic import BaseModel,Field
from typing import List,Optional


class ActorCreateRequest(BaseModel):
    fistName:str
    lastName:str
    birth_date: datetime.date
    patronymic:str
    star:int 
    


class ActorUpdateRequest(BaseModel):
    fistName:Optional[str] =None 
    lastName:Optional[str] =None 
    patronymic:Optional[str] =None 
    star:Optional[int] = None
    birth_date:Optional[datetime.date] = None 
    update_date:Optional[datetime.datetime] = None
    

class ActorResponse(BaseModel):
    id:uuid.UUID
    fistName:Optional[str] =None 
    lastName:Optional[str] =None 
    patronymic:Optional[str] =None 
    star:Optional[int] = None
    birth_date:Optional[datetime.date] =   None
    create_date:Optional[datetime.datetime] = None
    update_date:Optional[datetime.datetime] = None
    model_config = {
        "from_attributes": True
    }


class ActorListResponse(BaseModel):
    actors:List[ActorResponse]

