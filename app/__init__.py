from flask import Flask, render_template_string, send_from_directory, jsonify
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from app.extensions import db, migrate

from .config import Config
from .models import *

from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(Exception)
    def handle_all_errors(err):
        status = 500
        message = "Internal Server Error"

        if isinstance(err, KeyError):
            status = 400
            message = f"Missing key: {err}"
        elif isinstance(err, ValueError):
            status = 422  # Unprocessable Entity
            message = str(err)

        elif isinstance(err, Unauthorized):
            status = 401
            message = "Unauthorized"
        elif isinstance(err, Forbidden):
            status = 403
            message = "Forbidden"

        elif isinstance(err, (NotFound, NoResultFound)):
            status = 404
            message = str(err) or "Resource not found"

        elif isinstance(err, MultipleResultsFound):
            status = 500
            message = "Multiple results found when exactly one expected"

        elif hasattr(err, "status_code"):
            status = getattr(err, "status_code", 500)
            message = str(err)

        return jsonify(
            {
                "error": message,
                "status": status,
                "type": err.__class__.__name__,
            }
        ), status

    app.register_blueprint(main)

    # --- Swagger UI route ---
    @app.route("/docs")
    def swagger_ui():
        return render_template_string("""
        <!DOCTYPE html>
        <html>
          <head>
            <title>API Docs</title>
            <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
          </head>
          <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
              const ui = SwaggerUIBundle({
                url: '/openapi/f1.yml',
                dom_id: '#swagger-ui'
              });
            </script>
          </body>
        </html>
        """)

    # --- Static OpenAPI YAML route ---
    @app.route("/openapi/<path:filename>")
    def openapi_spec(filename):
        return send_from_directory("openapi", filename)

    return app
