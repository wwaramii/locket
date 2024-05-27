from datetime import datetime
from typing import AnyStr, Optional

from .base import CustomBaseModel
from .enums import Languages


class User(CustomBaseModel):
    """
    document_pack and key would be cleared after 5 minutes each time user logs in.
    """
    user_id: int
    language: Languages | None = None
    document_pack: Optional['DocumentPack'] = None
    key: AnyStr | None = None
    last_login: datetime | None = None



class DocumentPack(CustomBaseModel):
    """
    we would not save any user id or secret phrase.
    """
    identifier: AnyStr # this will be generated using telegram user id and secret phrase.


class Document(CustomBaseModel):
    """
    title can be a short description for the stored document.
    encrypted data can be decrypted using user_id and secret phrase.
    """
    document_pack_identifier: AnyStr
    title: AnyStr
    encrypted_data: AnyStr
