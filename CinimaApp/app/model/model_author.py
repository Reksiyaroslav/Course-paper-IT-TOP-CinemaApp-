
import datetime
import uuid
from  pydantic import BaseModel
from typing import List,Optional

class AuthorCreateRequest(BaseModel):
    fistname:str
    lastname:str
    birth_date: datetime.date
    patronymic:str
    bio:str  
    


class AuthorUpdateRequest(BaseModel):
    fistname:Optional[str] =None 
    lastname:Optional[str] =None 
    patronymic:Optional[str] =None 
    bio:Optional[str] = None
    birth_date:Optional[datetime.date] = None 
   
    

class AuthorResponse(BaseModel):
    id:uuid.UUID
    fistname:Optional[str] =None 
    lastname:Optional[str] =None 
    patronymic:Optional[str] =None 
    bio:Optional[str] = None
    birth_date:Optional[datetime.date] = None 
    created_at:Optional[datetime.datetime] = None
    update_at:Optional[datetime.datetime] = None
    model_config = {
        "from_attributes": True
    }

class AuthorlListResponse(BaseModel):
    author:List[AuthorResponse]

