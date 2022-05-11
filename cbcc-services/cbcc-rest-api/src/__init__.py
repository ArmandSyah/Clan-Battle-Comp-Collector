import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

# extensions
db = SQLAlchemy()

def create_app(script_info=None):

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    from src.resources import api
    api.init_app(app)
    
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db":db}

    return app