"""This module will contain utility functions to be used by the rest of the application"""

from werkzeug.security import generate_password_hash, check_password_hash

def hello_world():
    '''Simple Hello World Function'''
    return "Hello World!"
