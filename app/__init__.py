"""Smart Appointment Booking - Flask application factory."""
import os

from flask import Flask

from . import db, routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Secrets come from environment variables, never from the repository.
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.environ.get(
            "DATABASE_PATH", os.path.join(app.instance_path, "booking.sqlite")
        ),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)

    db.init_app(app)
    with app.app_context():
        db.init_db()

    app.register_blueprint(routes.bp)
    return app
