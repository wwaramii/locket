"""
database related exceptions.
"""

from typing import Dict
from safe_pass.db.base import DBBase


class DataBaseBaseException(Exception):
    def __init__(self, _from: DBBase, message: str) -> None:
        super().__init__(f"DBException from {_from.__class__.__name__}: {message}")


class DocumentNotFoundError(DataBaseBaseException):
    MESSAGE = "Could not found the specified document with query: {}"
    def __init__(self, _from: DBBase, query: Dict) -> None:
        super().__init__(_from, self.MESSAGE.format(query))
    
    
class OutrangeStartLimit(DataBaseBaseException):
    MESSAGE = "{} is out of range."
    def __init__(self, _from: DBBase, start: int) -> None:
        super().__init__(_from, self.MESSAGE.format(start))
    

class CouldNotDelete(DataBaseBaseException):
    ...
