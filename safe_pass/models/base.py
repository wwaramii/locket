from pydantic import BaseModel, Field, BeforeValidator
from pantherdb import PantherDB
from typing import AnyStr, List, Optional, Annotated


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    """
    All data are stored based on the owner(user).
    we would not save any user id or secret phrase.
    """
    id: Optional[PyObjectId | int | str] = Field(alias="_id", default=None)
    identifier: AnyStr # this will be generated using telegram user id and secret phrase.
    documents: List['Document'] = []

    class Config:
        populate_by_name = True
        from_attributes = True


class Document(BaseModel):
    """
    title can be a short description for the stored document.
    encrypted data can be decrypted using user_id and secret phrase.
    """
    title: AnyStr
    encrypted_data: AnyStr
