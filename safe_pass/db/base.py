from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict
from safe_pass.models import User, DocumentPack, Document


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
    
    @abstractmethod
    async def create_document(self, doc: Document) -> Document:
        ...
    
    @abstractmethod
    async def update_doc(self, query: Dict, doc: Document) -> Document:
        ...
    
    @abstractmethod
    async def read_one_doc(self, query: Dict) -> Document:
        ...
    
    @abstractmethod
    async def read_many_docs(self, query: Dict, start: int = 0, end: int=-1) -> AsyncIterator[Document]:
        ...
    
    @abstractmethod
    async def delete_doc(self, query: Dict) -> bool:
        ...
