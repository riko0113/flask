from flask import Flask
from apps.config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

csrf = CSRFProtect()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csef.init_app(app)
    db.init_app(app)
    Migrate(app, db)    

    login_manager.init_app(app)

    from apps.crud import views as crud_views
    form apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
