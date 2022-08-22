import logging
from flask import jsonify, make_response, request
from wotsong.api import api
from wotsong.api.utils.route_wrappers import require_auth
from wotsong.core.database import create_entity, db, update_entity
from wotsong.core.database.User import User, UserSchema
from wotsong.core.services.firebase import Firestore
from wotsong.core.utils import camel_to_snake, validate_schema
from flask_cors import cross_origin


@api.route('/me', methods=["GET"])
@require_auth()
def get_authed_user(user_id):
    user: User = User.query.get(user_id)
    if not user:
        user = create_entity(User, {"id": user_id})
        db.session.commit()
    return make_response(jsonify(user.as_camel_dict()), 200)

@api.route('/me', methods=["POST"])
@require_auth()
def update_authed_user(user_id):
    payload = camel_to_snake(request.json)
    user = User.query.get_or_404(user_id)
    try:
        update_entity(user, payload)
        db.session.commit()
        user = User.query.get(user_id)
        return make_response(jsonify(user.as_camel_dict()), 200)
    except Exception as e:
        logging.error(str(e))
        return make_response(jsonify({"message": "failed"}), 400)
