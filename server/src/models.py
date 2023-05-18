'''Database Models'''

from datetime import datetime

from config import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    '''User Table'''
    __tablename__ = "authors"

    id = db.Column(db.String(32), primary_key=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)

    register_date = db.Column(db.DateTime(), unique=False, default=datetime.now())
    admin = db.Column(db.Boolean, default=False)

    avatar = db.Column(db.String(64), unique=False, nullable=True, default=None)

    @property
    def password(self):
        '''Ensure Password is not Readable'''
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        '''Passwords will be hashed'''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''To compare passwords, we must check the hash.'''
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password):
        self.id = uuid4().hex
        self.username = username
        self.password_hash = generate_password_hash(password)
