"""rps flask app main file"""

from flask import Flask
from src.routes import rps_routes

def create_app():
    '''Initialize Flask App'''
    _app = Flask(__name__)
    _app.register_blueprint(rps_routes)

    #with app.app_context():
        # create handlers
        # create db connections

    return _app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
