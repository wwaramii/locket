from typing import Any, AsyncIterator, Dict
from pantherdb import PantherDB
from safe_pass.db.base import DBBase
from safe_pass.db.exceptions import DocumentNotFoundError, OutrangeStartLimit, CouldNotDelete
from safe_pass.models import User, DocumentPack, Document


class Panther(DBBase, PantherDB):
    __is_initialized: bool = False
    __instance = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.__instance:
            return super().__call__(*args, **kwds)
        return self.__instance

    
    def __init__(self,
            db_name: str = "safe_pass.pdb",
            user_collection: str = "users",
            doc_packs_collection: str = "doc_packs",
            docs_collection: str = "docs",
            *,
            return_dict: bool = False,
            return_cursor: bool = False,
            secret_key: bytes | None = None):
        if not self.__is_initialized:
            super().__init__(db_name, 
                             return_dict=return_dict, 
                             return_cursor=return_cursor, 
                             secret_key=secret_key)
            self.users_collection = self.collection(user_collection)
            self.doc_packs_collection = self.collection(doc_packs_collection)
            self.docs_collection = self.collection(docs_collection)
            self.__is_initialized = True

    async def create_user(self, user: User) -> User:
        doc = self.users_collection.insert_one(**user.model_dump())
        return User.model_validate(doc)
    
    async def update_user(self, query: Dict, user: User) -> User:
        is_updated = self.users_collection.update_one(query, **user.model_dump())
        if not is_updated:
            raise DocumentNotFoundError(_from=self, query=query)
        return user
    
    async def read_one_user(self, query: Dict) -> User:
        doc = self.users_collection.find_one(**query)
        if not doc:
            raise DocumentNotFoundError(_from=self, query=query)
        return User.model_validate(doc)

    async def create_doc_pack(self, doc_pack: DocumentPack) -> DocumentPack:
        doc = self.doc_packs_collection.insert_one(**doc_pack.model_dump())
        return DocumentPack.model_validate(doc)
    
    async def update_doc_pack(self, query: Dict, doc_pack: DocumentPack) -> DocumentPack:
        is_updated = self.doc_packs_collection.update_one(query, **doc_pack.model_dump())
        if not is_updated:
            raise DocumentNotFoundError(_from=self, query=query)
        return doc_pack
    
    async def read_one_doc_pack(self, query: Dict) -> DocumentPack:
        doc = self.doc_packs_collection.find_one(**query)
        if not doc:
            raise DocumentNotFoundError(_from=self, query=query)
        return DocumentPack.model_validate(doc)

    async def create_document(self, doc: Document) -> Document:
        doc = self.docs_collection.insert_one(**doc.model_dump())
        return Document.model_validate(doc)
    
    async def update_doc(self, query: Dict, doc: Document) -> Document:
        is_updated = self.docs_collection.update_one(query, **doc.model_dump())
        if not is_updated:
            raise DocumentNotFoundError(_from=self, query=query)
        return doc
    
    async def read_one_doc(self, query: Dict) -> Document:
        if query.get('id'):
            query['_id'] = query.pop('id')
        doc = self.docs_collection.find_one(**query)
        if not doc:
            raise DocumentNotFoundError(_from=self, query=query)
        return Document.model_validate(doc)
    
    async def read_many_docs(self, query: Dict, start: int = 0, end: int=-1) -> AsyncIterator[Document]:
        if query.get('id'):
            query['_id'] = query.pop('id')
        
        docs = self.docs_collection.find(**query)
        if start != 0 and start > (len(docs) -1):
            raise OutrangeStartLimit(self, start)
        for doc in docs[start:end]:
            yield Document.model_validate(doc)
    
    async def delete_doc(self, query: Dict) -> bool:
        if query.get('id'):
            query['_id'] = query.pop('id')
        
        result = self.docs_collection.delete_one(**query)
        if not result:
            raise CouldNotDelete(self, f"Could not delete document with query {query}")
        return True
