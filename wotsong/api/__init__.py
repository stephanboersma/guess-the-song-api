from flask import Blueprint
print(__name__)

api = Blueprint("api", __name__, url_prefix="/api")

from . import users