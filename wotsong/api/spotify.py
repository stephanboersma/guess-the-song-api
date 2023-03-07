from datetime import datetime, timedelta
from wotsong.api import api
from wotsong.api.utils.route_wrappers import require_auth
from wotsong.core.database import create_entity, db, firestore_db, update_entity
from wotsong.core.database.User import SpotifyAccessToken, SpotifyAuthRequest, SpotifySecret, User
from wotsong.core.services.spotify import spotify
from flask import redirect, request, make_response, jsonify
from flask_cors import cross_origin
from wotsong.core.utils import camel_to_snake



@api.route('/spotify/connect', methods=["GET"])
def spotify_login():
    return redirect(spotify.get_auth_url())


@api.route('/spotify/token', methods=["POST"])
@cross_origin()
@require_auth()
def authenticate_with_spotify(user_id):
    payload = camel_to_snake(request.json)
    try:
        SpotifyAuthRequest().validate(payload)
    except Exception as e:
        return make_response(str(e), 400)
    credentials = spotify.authenticate_user(payload["code"])
    credentials["user_id"] = user_id
    payload = {
        "user_id": user_id,
        "refresh_token": credentials["refresh_token"],
        "expires_at": datetime.utcnow() + timedelta(hours=1)
    }
    create_entity(SpotifySecret, payload)
    db.session.commit()
    firestore_db.set_document(SpotifyAccessToken(user_id, credentials["access_token"], payload["expires_at"]))
    return make_response("OK", 200)

@api.route('/spotify/token/refresh', methods=["POST"])
@cross_origin()
@require_auth()
def refresh_spotify_token(user_id):
    spotify.refresh_user_access_token(user_id)
    return make_response("OK", 200)
    