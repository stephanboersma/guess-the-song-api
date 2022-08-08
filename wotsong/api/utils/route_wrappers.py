from wotsong.core.services.firebase import Firestore
from wotsong.core.models import User
from functools import wraps
from flask import current_app, request, jsonify, make_response
import wotsong.core

db: Firestore = wotsong.core.db

def require_auth():
    def decorator(resolver_function):
        @wraps(resolver_function)
        def decorator(*args, **kwargs):
            print(db)
            token = None
            if "x-access-token" in request.headers:
                token = request.headers.get("x-access-token")
            if not token:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            try:
                user_id = db.verify_id_token(token)
            except:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            return resolver_function(user_id, *args, **kwargs)
        return decorator
    return decorator
