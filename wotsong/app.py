from venv import create
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
import logging
from os import environ as env, getpid
from flask_cors import CORS
from .api import api
from .core.database import init_db

logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()
logger.info(f'Starting app in {env["APP_ENV"]} environment')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@localhost:5432/wotsong'
    register_extensions(app)
    return app


def register_extensions(app):
    init_db(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    app.register_blueprint(api)
    print(app.url_map)
    
    
    
    




