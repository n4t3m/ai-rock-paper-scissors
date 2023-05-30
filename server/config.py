'''Flask Configuration Config'''

from os import urandom
from flask_sqlalchemy import SQLAlchemy
from queue import Queue

db = SQLAlchemy()

class FlaskConfig:
    '''Flask Configuration Class'''
    # SERVER_NAME = "localhost.localdomain"
    SECRET_KEY = urandom(32).hex()

    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    QUEUE = Queue()
