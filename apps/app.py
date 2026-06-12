from flask import Flask
from apps.config import config
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csef.init_app(app)
    db.init_app(app)
    Migrate(app, db)    

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
