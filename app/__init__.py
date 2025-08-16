from flask import Flask, render_template_string, send_from_directory

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
