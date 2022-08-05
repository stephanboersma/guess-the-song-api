from wotsong.core.services.firebase import Firestore
from functools import wraps
from flask import request, jsonify, make_response



def require_auth(firestore: Firestore):
    def decorator(resolver_function):
        @wraps(resolver_function)
        def decorator(*args, **kwargs):
            token = None
            if "x-access-token" in request.headers:
                token = request.headers.get("x-access-token")
            if not token:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            try:
                user_uid = firestore.verify_id_token(token)
            except:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            return resolver_function(user_uid, *args, **kwargs)
        return decorator
    return decorator
