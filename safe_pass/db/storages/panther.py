from typing import Any, Dict
from pantherdb import PantherDB
from safe_pass.db.base import DBBase
from safe_pass.db.exceptions import DocumentNotFoundError
from safe_pass.models import User, DocumentPack


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
        return User.model_validate(**doc)

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
        return DocumentPack.model_validate(**doc)
