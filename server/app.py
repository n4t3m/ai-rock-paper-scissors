"""rps flask app main file"""

from os import urandom

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from src.routes import rps_routes
from src.models import User
from src.util import playMatches
from config import FlaskConfig, db

def create_app():
    '''Initialize Flask App'''
    # Initialize Flask
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    #print(app.config)

    # Register API Routes
    app.register_blueprint(rps_routes)

    # Init Match Scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(playMatches, 'interval', seconds=5, args=(app,))
    scheduler.start()

    # Initialize DB
    db.init_app(app)
    with app.app_context():
        # create db based on imported models
        db.drop_all()
        db.create_all()

        secret = urandom(16).hex()

        db.session.add(User(
            username="admin",
            password=secret,
        ))

        print(f"Randomly generated admin password: {secret}")
        secret = urandom(16).hex()

        db.session.add(User(
            username="nano_one",
            password=secret,
        ))

        print(f"Randomly generated nano_one password: {secret}")
        secret = urandom(16).hex()

        db.session.add(User(
            username="nano_two",
            password=secret,
        ))

        print(f"Randomly generated nano_two password: {secret}")
        secret = None

        # Create Sample Data Here
        db.session.commit()

        # Create handlers to be used


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
