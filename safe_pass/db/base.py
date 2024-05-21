from abc import ABC, abstractmethod
from typing import Dict
from safe_pass.models import User, DocumentPack


class DBBase(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        ...
    
    @abstractmethod
    async def update_user(self, query: Dict, user: User) -> User:
        ...
    
    @abstractmethod
    async def read_one_user(self, query: Dict) -> User:
        ...

    @abstractmethod
    async def create_doc_pack(self, doc_pack: DocumentPack) -> DocumentPack:
        ...
    
    @abstractmethod
    async def update_doc_pack(self, query: Dict, doc_pack: DocumentPack) -> DocumentPack:
        ...
    
    @abstractmethod
    async def read_one_doc_pack(self, query: Dict) -> DocumentPack:
        ...
    
    # TODO: delete a doc_pack
