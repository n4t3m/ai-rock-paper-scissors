'''This module contains API calls for the RPS Game'''

from flask import Blueprint
from src.util import hello_world

rps_routes = Blueprint("rps_routes", __name__)

@rps_routes.route("/", methods=["GET"])
def hello_world_route():
    '''Simple Hello World API Call'''
    return hello_world()
