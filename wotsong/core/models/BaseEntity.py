
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional, Protocol

class EntityNotCommited(Exception):
    pass

class BaseEntity(Protocol):
    id: str

    @property
    def path(self) -> str:
        return self.__class__.get_document_reference(self.id).get_path()

    @staticmethod
    def get_document_reference(id: str = None) -> DocumentReference:
        raise NotImplementedError()

    def to_dict(self) -> dict:
        dictionary:dict = asdict(self)
        return {
            key: dictionary.get(key) for key in dictionary if "__" not in key
        }

@dataclass
class DocumentReference:
    collection_path: str
    id: Optional[str] = None

    @property
    def is_committed(self) -> bool:
        return self.id is not None

    def get_path(self) -> str:
        if not self.is_committed:
            raise EntityNotCommited("Entity not committed. Cannot get path with id")
        return f"{self.collection_path}/{self.id}"

    

    