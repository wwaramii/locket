from typing import Any, Dict
from pantherdb import PantherDB
from safe_pass.db.base import DBBase
from safe_pass.db.exceptions import DocumentNotFoundError
from safe_pass.models.base import User


class Panther(DBBase, PantherDB):
    __is_initialized: bool = False
    __instance = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.__instance:
            return super().__call__(*args, **kwds)
        return self.__instance

    
    def __init__(self,
            db_name: str = "safe_pass.pdb",
            main_collection: str = "main",
            *,
            return_dict: bool = False,
            return_cursor: bool = False,
            secret_key: bytes | None = None):
        if not self.__is_initialized:
            super().__init__(db_name, 
                             return_dict=return_dict, 
                             return_cursor=return_cursor, 
                             secret_key=secret_key)
            self.main_collection = self.collection(main_collection)
            self.__is_initialized = True

    async def create_user(self, user: User) -> User:
        doc = self.main_collection.insert_one(**user.model_dump())
        return User.model_validate(doc)
    
    async def update_user(self, query: Dict, user: User) -> User:
        is_updated = self.main_collection.update_one(query, **user.model_dump())
        if not is_updated:
            raise DocumentNotFoundError(_from=self, query=query)
        return user
    
    async def read_one(self, query: Dict) -> User:
        doc = self.main_collection.find_one(**query)
        if not doc:
            raise DocumentNotFoundError(_from=self, query=query)
        return User.model_validate(**doc)
