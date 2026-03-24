from pydantic import BaseModel
from datetime import datetime


class BaseSheman(BaseModel):
    model_config = {"from_attributes": True}


class TimestampMixin(BaseSheman):
    created_at: datetime | None = None
    updated_at: datetime | None = None
