from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from apps.config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask import redirect, url_for


csrf = CSRFProtect()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = ""

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)    

    login_manager.init_app(app)

    from apps.crud import views as crud_views
    from apps.auth import views as auth_views
    from apps.face import views as face_views
    from apps.detector import views as detector_views
    from apps.kids import views as kids_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.register_blueprint(face_views.face, url_prefix="/face")
    app.register_blueprint(detector_views.detector, url_prefix="/detector")
    app.register_blueprint(kids_views.kids,url_prefix="/kids")

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app
