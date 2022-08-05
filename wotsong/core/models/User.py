
from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import Optional
from .BaseEntity import BaseEntity, DocumentReference

SPOTIFY_SECRETS_ID = "spotify_secrets"
SECRETS_COLLECTION_NAME = "secrets"

@dataclass
class User(BaseEntity):
    id: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    __COLLECTION_NAME: str = field(default="users",init=False)

    @property
    def is_anonymous(self) -> str:
        return self.email is None

    def get_secrets_reference(self) -> DocumentReference:
        return DocumentReference(collection_path=f"{self.path}/{SECRETS_COLLECTION_NAME}", id=SPOTIFY_SECRETS_ID) 

    def get_document_reference(id: str = None) -> DocumentReference:
        return DocumentReference(collection_path=User.__COLLECTION_NAME, id=id)

    

@dataclass
class SpotifySecrets(BaseEntity):
    spotity_access_token: str
    spotify_token_expire_date: datetime
    spotify_refresh_token: str
    id: str = SPOTIFY_SECRETS_ID
    __user: User = field(default=None, init=False)

    def set_user(self, user: User) -> None:
        self.__user = user

    def get_document_reference(self) -> DocumentReference:
        return DocumentReference(collection_path=f"{self.__user.path}/{SECRETS_COLLECTION_NAME}", id=SPOTIFY_SECRETS_ID)




