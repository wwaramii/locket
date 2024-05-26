from typing import Dict
from pydantic import BaseModel, Field

from .base import PyObjectId


class Statics(BaseModel):
    id: PyObjectId | int | str = Field(alias="_id", default=None)
    images: Dict[str, str]

    class Config:
        from_attributes = True
        populate_by_name = True

