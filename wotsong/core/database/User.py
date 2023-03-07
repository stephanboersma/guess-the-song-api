from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .TimestampMixin import TimestampMixin
from wotsong.core.services.firebase import FirebaseEntity, DocumentReference
from wotsong.core.database import db
from marshmallow import fields, Schema
SECRETS_COLLECTION_NAME = "spotify_access_tokens"

class UserSchema(Schema):
    id = fields.Str(required=True)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    alias = fields.Str(required=False)
    email = fields.Str(required=False)

class SpotifySecretSchema(Schema):
    user_id: fields.Str(required=True)
    refresh_token: fields.Str(required=True)
    expires_at: fields.DateTime(required=True)



class User(TimestampMixin, db.Model):
    id: str = Column(String, primary_key=True)
    first_name: str = Column(String, nullable=True)
    last_name:str = Column(String, nullable=True)
    alias:str = Column(String, nullable=True)
    email: str = Column(String, nullable=True)
    spotify_secret: SpotifySecret = relationship('SpotifySecret', uselist=False, lazy=True)
    schema = UserSchema()

    @property
    def is_anonymous(self) -> str:
        return self.email is None

class SpotifySecret(TimestampMixin, db.Model):
    id: int = Column(Integer, primary_key=True)
    user_id: str = Column(String, ForeignKey(User.id), nullable=False)
    refresh_token: str = Column(String, nullable=False)
    expires_at: datetime = Column(DateTime, nullable=False)
    schema = SpotifySecretSchema()


class SpotifyAuthRequest(Schema):
    code = fields.Str(required=True)

@dataclass
class SpotifyAccessToken(FirebaseEntity):
    id: str
    access_token: str
    expires_at: datetime

    def get_document_reference(self) -> DocumentReference:
        return DocumentReference(collection_path=f"{SECRETS_COLLECTION_NAME}", id=self.id)




