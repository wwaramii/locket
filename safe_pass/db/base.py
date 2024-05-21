from abc import ABC, abstractmethod
from typing import Dict
from safe_pass.models.base import User


class DBBase(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        ...
    
    @abstractmethod
    async def update_user(self, query: Dict, user: User) -> User:
        ...
    
    @abstractmethod
    async def read_one(self, query: Dict) -> User:
        ...

    # TODO: delete a user
