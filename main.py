from dataclasses import asdict
from datetime import datetime
from typing import List
from wotsong.core.models import User, SpotifySecrets
from wotsong.core.services.firebase import Firestore
fb = Firestore()
user = User("1234")
secret = SpotifySecrets("1", datetime.now(), "2")
secret.set_user(user)

print(user.to_dict())
fb.set_document(user)
fb.set_document(secret)
ref: User = fb.get_document(User, User.get_document_reference("1234"))

secret_ref = ref.get_secrets_reference()

secrets: SpotifySecrets = fb.get_document(SpotifySecrets, secret_ref)

print(ref.to_dict())
