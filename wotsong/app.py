from flask import Flask, jsonify, make_response
from dotenv import load_dotenv

from wotsong.core.services.firebase import Firestore

load_dotenv()
import logging
from os import environ as env, getpid
from flask_cors import CORS
import wotsong.core
wotsong.core.db = Firestore()
from .api import api

logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()
logger.info(f'Starting app in {env["APP_ENV"]} environment')


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


app.register_blueprint(api)
print(app.url_map)


@app.route('/')
def hello_world():
   return 'Hello, World!'