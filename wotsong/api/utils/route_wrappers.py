from wotsong.core.services.firebase import Firestore
from wotsong.core.database import User
from functools import wraps
from flask import request, jsonify, make_response
from wotsong.core.database import firestore_db as fire_db
import flask

TOKEN_HEADER = "Authorization"

firestore_db: Firestore = fire_db

def require_auth():
    def decorator(resolver_function):
        @wraps(resolver_function)
        def decorator(*args, **kwargs):
            token = None
            if TOKEN_HEADER in request.headers:
                token = request.headers.get(TOKEN_HEADER)
            if not token:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            try:
                token = token.replace("Bearer ", "")
                user_id = firestore_db.verify_id_token(token)
            except:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            return resolver_function(user_id, *args, **kwargs)
        return decorator
    return decorator


