'''Flask Configuration Config'''

from os import urandom
from queue import Queue

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FlaskConfig:
    '''Flask Configuration Class'''
    # SERVER_NAME = "localhost.localdomain"
    SECRET_KEY = urandom(32).hex()

    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    QUEUE = Queue()
