import logging
from flask import current_app, jsonify, make_response, request
from wotsong.api import api
from wotsong.api.utils.route_wrappers import require_auth
from wotsong.core.models.User import User
from wotsong.core.services.firebase import Firestore
import wotsong.core

db: Firestore = wotsong.core.db

@api.route('/me', methods=["GET"])
@require_auth()
def get_authed_user(user_id):
    try:
        user: User = db.get_document(User, User.get_document_reference(user_id))
        return make_response(jsonify(user.to_dict()), 200)
    except:
        return make_response(jsonify({"message": "failed"}), 400)

@api.route('/me', methods=["PUT"])
@require_auth()
def update_authed_user(user_id):
    try:
        print(request.json)
        user: User = db.update_document(User, User.get_document_reference(user_id), request.json)
        return make_response(jsonify(user.to_dict()), 200)
    except Exception as e:
        logging.error(str(e))
        return make_response(jsonify({"message": "failed"}), 400)

@api.route('/users', methods=["POST"])
@require_auth()
def create_user(user_id):
    body = request.json
    user = User(user_id, body["displayName"], body["email"])
    try:
        user: User = db.set_document(user)
        return make_response(jsonify(user.to_dict()), 201)
    except:
        return make_response(jsonify({"message": "failed"}), 400)
    
