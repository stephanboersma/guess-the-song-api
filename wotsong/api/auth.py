from datetime import datetime, timedelta
import logging
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from wotsong.api import api
from wotsong.api.utils.route_wrappers import require_auth
from wotsong.core.database import create_entity, db, update_entity
from wotsong.core.database.User import SpotifySecret, User
from wotsong.core.utils import camel_to_snake
from wotsong.core.services.spotify import spotify

@api.route('/me', methods=["GET"])
@require_auth()
def get_authed_user(user_id):
    user: User = User.query.get(user_id)
    if not user:
        return make_response({"message": "Not found"}, 404)
    spotify_secret: SpotifySecret = SpotifySecret.query.filter_by(user_id=user_id).first()
    
    if spotify_secret:
        if datetime.utcnow() > spotify_secret.expires_at:
            spotify.refresh_user_access_token(user_id)
    return make_response(jsonify(user.as_camel_dict()), 200)


@api.route('/me', methods=["POST"])
def update_authed_user():
    payload = camel_to_snake(request.json)
    try:
        create_entity(User, payload)
        db.session.commit()
        user = User.query.get(payload["id"])
        return make_response(jsonify(user.as_camel_dict()), 201)
    except Exception as e:
        logging.error(str(e))
        return make_response(jsonify({"message": "failed"}), 400)
