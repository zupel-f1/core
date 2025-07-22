from flask import Flask

from app.extensions import db, migrate

from .config import Config
from .models import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app
