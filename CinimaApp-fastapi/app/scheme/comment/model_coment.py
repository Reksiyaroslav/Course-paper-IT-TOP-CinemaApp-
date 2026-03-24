import datetime
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from app.scheme.user.user_base import UserReponseNotInfo
from app.scheme.comment.comment_base import ComenntBase


class ComentCreateRequest(ComenntBase):
    pass


class ComentUpdateRequest(ComenntBase):
    pass


class ComentResponse(ComenntBase):
    coment_id: uuid.UUID
    description: Optional[str] = None
    countheart: Optional[int] = Field(default=0)
    countdemon: Optional[int] = Field(default=0)
    created_at: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    model_config = {"from_attributes": True}


class ComentWithUserResponse(ComentResponse):
    user: Optional[UserReponseNotInfo] = None


class ComentListReponse(BaseModel):
    comments: List[ComentResponse] = None


class ComentsListFilmIds(BaseModel):
    film_ids: List[uuid.UUID]


class ComentsListUserIds(BaseModel):
    user_ids: List[uuid.UUID]
