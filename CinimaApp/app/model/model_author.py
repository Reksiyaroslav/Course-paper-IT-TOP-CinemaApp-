
import datetime
import uuid
from  pydantic import BaseModel
from typing import List,Optional

class AuthorCreateRequest(BaseModel):
    fistName:str
    lastName:str
    birth_date: datetime.date
    patronymic:str
    bio:str  
    


class AuthorUpdateRequest(BaseModel):
    fistName:Optional[str] =None 
    lastName:Optional[str] =None 
    patronymic:Optional[str] =None 
    bio:Optional[str] = None
    birth_date:Optional[datetime.date] = None 
    update_date:Optional[datetime.datetime] = None
    

class AuthorResponse(BaseModel):
    id:uuid.UUID
    fistName:Optional[str] =None 
    lastName:Optional[str] =None 
    patronymic:Optional[str] =None 
    bio:Optional[str] = None
    birth_date:Optional[datetime.date] = None 
    create_date:Optional[datetime.datetime] = None
    update_date:Optional[datetime.datetime] = None
    model_config = {
        "from_attributes": True
    }

class AuthorlListResponse(BaseModel):
    author:List[AuthorResponse]

