from __future__ import annotations

from typing import Type, Optional, Protocol
import firebase_admin
from firebase_admin import firestore, auth
from dataclasses import asdict, dataclass

firebase_app = firebase_admin.initialize_app()

class DocumentNotFound(Exception):
    pass

class EntityNotCommited(Exception):
    pass

class FirebaseEntity(Protocol):
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


class Firestore:

    db = firestore.client()

    def add_document(self, entity: FirebaseEntity):
        if entity.is_committed:
            raise Exception("This is not a new object")
        document_reference = entity.get_document_reference()
        ref = self.db.collection(document_reference.collection_path).add(entity.to_dict())
        setattr(entity, "id", ref[1].id)
        return entity

    def set_document(self, entity: FirebaseEntity):
        document_reference = entity.get_document_reference()
        ref = self.db.collection(document_reference.collection_path).document(entity.id).set(entity.to_dict())
        return entity

    def update_document(self, cls: Type[FirebaseEntity], ref: DocumentReference, payload):
        self.db.collection(ref.collection_path).document(ref.id).set(payload,merge=True)
        return self.get_document(cls, ref)

    def delete_document(self, entity: FirebaseEntity):
        document_reference = entity.get_document_reference()
        self.db.collection(document_reference.collection_path).document(entity.id).delete()

    def get_document(self, cls: Type[FirebaseEntity], ref: DocumentReference):
        document = self.db.collection(ref.collection_path).document(ref.id).get()
        if not document.exists:
            raise DocumentNotFound()
        return cls(**document.to_dict())


    def get_collection(self, cls: Type[FirebaseEntity]):
        ref = cls.get_document_reference()
        query = self.db.collection(ref.collection_path).stream()
        return [ cls(**document.to_dict()) for document in query]

    def verify_id_token(self, token) -> str:
        identity = auth.verify_id_token(token)
        return identity["uid"] or None