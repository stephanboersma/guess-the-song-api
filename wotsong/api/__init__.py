from flask import Blueprint
from flask_cors import CORS

api = Blueprint("api", __name__, url_prefix="/api")

from . import auth
from . import spotify