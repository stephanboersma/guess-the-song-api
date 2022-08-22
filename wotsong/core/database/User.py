
from dataclasses import dataclass
from datetime import datetime
from typing import List
from sqlalchemy import Column, String
from .TimestampMixin import TimestampMixin
from wotsong.core.services.firebase import FirebaseEntity, DocumentReference
from wotsong.core.database import db
from marshmallow import fields, Schema
SECRETS_COLLECTION_NAME = "secrets"

class UserSchema(Schema):
    id = fields.Str(required=True)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    alias = fields.Str(required=False)
    email = fields.Str(required=False)

class User(TimestampMixin, db.Model):
    id: str = Column(String, primary_key=True)
    first_name: str = Column(String, nullable=True)
    last_name:str = Column(String, nullable=True)
    alias:str = Column(String, nullable=True)
    email: str = Column(String, nullable=True)
    schema = UserSchema()

    @property
    def is_anonymous(self) -> str:
        return self.email is None

    def get_secrets_reference(self) -> DocumentReference:
        return DocumentReference(collection_path=f"{SECRETS_COLLECTION_NAME}", id=self.id)


    

@dataclass
class SpotifySecrets(FirebaseEntity):
    id: str
    spotity_access_token: str
    spotify_token_expire_date: datetime
    spotify_refresh_token: str

    def get_document_reference(self) -> DocumentReference:
        return DocumentReference(collection_path=f"{SECRETS_COLLECTION_NAME}", id=self.id)




