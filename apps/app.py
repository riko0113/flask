from flask import Flask
from apps.config import config

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app