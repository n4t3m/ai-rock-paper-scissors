'''This module contains API calls for the RPS Game'''

from flask import Blueprint, session, abort, request
from src.util import hello_world
from src.decorators import login_required
from src.models import User

rps_routes = Blueprint("rps_routes", __name__)

@rps_routes.route("/", methods=["GET"])
def hello_world_route():
    '''Simple Hello World API Call'''
    return hello_world()


# @rps_routes.route("/login", methods=["GET"])
# def login():
#     '''Simple "Login" Route for testing, log into psuedo Guest User'''
#     session['username']="Guest"
#     return "You have been logged in!"

@rps_routes.route("/login", methods=["POST"])
def login():
    '''Login Route'''
    username = request.form.get("username")
    if not username:
        # print("Username Not Provided!")
        abort(400)
    password = request.form.get("password")
    if not password:
        # print("Password not Provided!")
        abort(400)

    user_record = User.query.filter_by(username=username).first()

    if user_record and user_record.verify_password(password):
        session['username']=username
        return "You have been logged in!"

    return "Username/Password Combination Not Found"

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
