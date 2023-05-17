'''This module contains API calls for the RPS Game'''

from flask import Blueprint, session, abort
from src.util import hello_world
from src.decorators import login_required

rps_routes = Blueprint("rps_routes", __name__)

@rps_routes.route("/", methods=["GET"])
def hello_world_route():
    '''Simple Hello World API Call'''
    return hello_world()

@rps_routes.route("/login", methods=["GET"])
def login():
    '''Simple "Login" Route'''
    session['username']="Guest"
    return "You have been logged in!"

@rps_routes.route("/logout", methods=["GET"])
def logout():
    '''Simple "Logout" Route'''
    if "username" in session:
        del session["username"]
        return "You have been logged out!"
    return abort(401)

@rps_routes.route("/auth_check", methods=["GET"])
@login_required
def protected_route():
    '''Simple Auth-Check Route'''
    return "You are authenticated!"
