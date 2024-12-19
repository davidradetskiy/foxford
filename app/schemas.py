from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class DateSort(str, Enum):
    asc = "asc"
    desc = "desc"


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class AppealSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    datetime: datetime
    email: str
    message: str
    user: UserSchema | None
