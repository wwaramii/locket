from pydantic import BaseModel, Field, BeforeValidator
from typing import  Annotated


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class CustomBaseModel(BaseModel):
    id: PyObjectId | int | str = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        from_attributes = True
