"""rps flask app main file"""

from flask import Flask
from src.routes import rps_routes
from src.models import User
from config import FlaskConfig, db

def create_app():
    '''Initialize Flask App'''
    # Initialize Flask
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    #print(app.config)

    # Register API Routes
    app.register_blueprint(rps_routes)

    # Initialize DB
    db.init_app(app)
    with app.app_context():
        # create db based on imported models
        db.create_all()

        db.session.add(User(
            username="admin",
            password="password",
        ))

        # Create Sample Data Here
        db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
