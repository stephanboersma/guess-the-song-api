from typing import Type
import firebase_admin
from firebase_admin import firestore, auth
from dataclasses import asdict

from wotsong.core.models.BaseEntity import BaseEntity, DocumentReference


firebase_app = firebase_admin.initialize_app()

class DocumentNotFound(Exception):
    pass


class Firestore:

    db = firestore.client()

    def add_document(self, entity: BaseEntity):
        if entity.is_committed:
            raise Exception("This is not a new object")
        document_reference = entity.get_document_reference()
        ref = self.db.collection(document_reference.collection_path).add(entity.to_dict())
        setattr(entity, "id", ref[1].id)
        return entity

    def set_document(self, entity: BaseEntity):
        document_reference = entity.get_document_reference()
        return self.db.collection(document_reference.collection_path).document(entity.id).set(entity.to_dict())

    def delete_document(self, entity: BaseEntity):
        document_reference = entity.get_document_reference()
        self.db.collection(document_reference.collection_path).document(entity.id).delete()

    def get_document(self, cls: Type[BaseEntity], ref: DocumentReference):
        document = self.db.collection(ref.collection_path).document(ref.id).get()
        if not document.exists:
            raise DocumentNotFound()
        return cls(**document.to_dict())


    def get_collection(self, cls: Type[BaseEntity]):
        ref = cls.get_document_reference()
        query = self.db.collection(ref.collection_path).stream()
        return [ cls(**document.to_dict()) for document in query]

    def verify_id_token(self, token) -> str:
        identity = auth.verify_id_token(token)
        return identity["uid"] or None