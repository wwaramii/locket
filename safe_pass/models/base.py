from datetime import datetime
from pydantic import BaseModel, Field, BeforeValidator
from typing import AnyStr, List, Optional, Annotated


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    """
    document_pack and key would be cleared after 5 minutes each time user logs in.
    """
    id: Optional[PyObjectId | int | str] = Field(alias="_id", default=None)
    user_id: int
    document_pack: 'DocumentPack' = None
    key: AnyStr = None
    last_login: datetime = None


class DocumentPack(BaseModel):
    """
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
