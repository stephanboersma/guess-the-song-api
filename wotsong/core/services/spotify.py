from datetime import datetime, timedelta
from os import environ as env
import requests
from wotsong.core.database import update_entity, db, firestore_db
from wotsong.core.database.User import SpotifyAccessToken, SpotifySecret

from wotsong.core.utils import base64_encode
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_AUTH_SCOPES = [
  'user-read-currently-playing',
  'user-read-playback-state',
  'user-modify-playback-state',
  'playlist-read-private',
  'playlist-read-collaborative',
  'streaming',
  'user-read-email',
  'user-read-private'
]

class Spotify:

    client_id: str
    client_secret: str
    redirect_uri: str
    
    def __init__(self) -> None:
        self.client_id = env["SPOTIFY_CLIENT_ID"]
        self.client_secret = env["SPOTIFY_CLIENT_SECRET"]
        self.redirect_uri = env["SPOTIFY_REDIRECT_URI"]

    def get_auth_url(self) -> str:
        scopes = "%20".join(SPOTIFY_AUTH_SCOPES)
        return f"{SPOTIFY_AUTH_URL}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={scopes}&response_type=code"

    def __get_authorization_header(self):
        encoded_credentials = base64_encode(f"{self.client_id}:{self.client_secret}")
        return f"Basic {encoded_credentials}"

    def authenticate_user(self, code):
        headers = {
            "Authorization": self.__get_authorization_header()
        }
        response = requests.post(url=SPOTIFY_TOKEN_URL, data={"code": code, "grant_type": "authorization_code", "redirect_uri": self.redirect_uri}, headers=headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(str(response.text))

    def refresh_user_access_token(self, user_id):
        spotify_secret: SpotifySecret = SpotifySecret.query.filter_by(user_id=user_id).first()
        credentials = self.get_access_token_by_refresh(spotify_secret.refresh_token)
        payload = {
            "expires_at": datetime.utcnow() + timedelta(minutes=45)
        }
        update_entity(spotify_secret, payload)
        db.session.commit()
        firestore_db.set_document(SpotifyAccessToken(user_id, credentials["access_token"], payload["expires_at"]))


    def get_access_token_by_refresh(self, refresh_token):
        headers = {
            "Authorization": self.__get_authorization_header()
        }
        response = requests.post(url=SPOTIFY_TOKEN_URL, data={"refresh_token": refresh_token, "grant_type": "refresh_token", "redirect_uri": self.redirect_uri}, headers=headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(str(response.text))

spotify = Spotify()

    
