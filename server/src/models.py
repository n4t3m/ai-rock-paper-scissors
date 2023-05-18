'''Database Models'''

from datetime import datetime

from config import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    '''User Table'''
    __tablename__ = "users"

    id = db.Column(db.String(32), primary_key=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)

    register_date = db.Column(db.DateTime(), unique=False, default=datetime.now())
    admin = db.Column(db.Boolean, default=False)

    elo = db.Column(db.Integer, unique=False, nullable=False)

    matches_as_player_one = db.relationship('MatchHistory', backref='player_one', foreign_keys='MatchHistory.player_one_id', lazy=True)
    matches_as_player_two = db.relationship('MatchHistory', backref='player_two', foreign_keys='MatchHistory.player_two_id', lazy=True)

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
        self.elo = 1000

class MatchHistory(db.Model):
    '''Match History Table'''
    __tablename__ = "matchhistory"

    match_id = db.Column(db.String(32), primary_key=True)

    # Many to One Relationship
    player_one_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    player_two_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)

    player_one_initial_elo = db.Column(db.Integer)
    player_two_initial_elo = db.Column(db.Integer)

    player_one_final_elo = db.Column(db.Integer)
    player_two_final_elo = db.Column(db.Integer)

    winner = db.Column(db.String(1), default="0")

    player_one_ack = db.Column(db.Boolean, default=False)
    player_two_ack = db.Column(db.Boolean, default=False)

    match_created = db.Column(db.DateTime(), unique=False, default=datetime.now())

    def __init__(self, player_one_id, player_two_id):

        player_one = User.query.get(player_one_id)
        if player_one is None:
            raise ValueError(f"Invalid player one ID: {player_one_id}")

        # Validate player_two_id
        player_two = User.query.get(player_two_id)
        if player_two is None:
            raise ValueError(f"Invalid player two ID: {player_two_id}")

        self.match_id = uuid4().hex
        self.player_one_id = player_one_id
        self.player_two_id = player_two_id
        self.player_one_final_elo = None
        self.player_two_final_elo = None
        self.player_one_initial_elo = User.query.get(player_one_id).elo
        self.player_two_initial_elo = User.query.get(player_two_id).elo
        self.winner = "0"
