from flask import Flask, jsonify, make_response
from dotenv import load_dotenv

load_dotenv()
import logging
from os import environ as env, getpid
from wotsong.core.services.firebase import Firestore
from wotsong.core.models.User import User
from wotsong.core.models.Game import Game
from .api import api

logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()
logger.info(f'Starting app in {env["APP_ENV"]} environment')
app = Flask(__name__)
app.register_blueprint(api)
print(app.url_map)
firestore = Firestore()

@app.route('/')
def hello_world():
   return 'Hello, World!'

@app.route('/user', methods=["POST"])
def create_user():
   user = User(
      uid="12345",
      display_name="Hund"
   )
   firestore.add_document('users', user)
   return make_response(jsonify({"message": "success"}), 200)

@app.route('/game', methods=["POST"])
@require_auth(firestore=firestore)
def create_game(user):
   print(user)
   game = Game()
   firestore.set_document('games', game.game_code, game)
   return make_response(jsonify({"message": "success"}), 200)