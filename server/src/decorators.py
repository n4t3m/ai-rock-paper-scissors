'''Decorators used throughout the program are writtin inside of this module'''

from functools import wraps
from flask import abort, session

def login_required(f):
    '''Auth Check Decorator'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function
