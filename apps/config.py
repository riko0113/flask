from pathlib import Path

basedir = Path(__file__).parent.parent.parent


class BaseConfig:
    SECRET_KEY = "ffa61fa8069020b2501550ebe83ff105"
    WTF_CSRF_SECRET_KEY = "5a5f0d6325d5e615a77ec3e875af9271"
    UPLOAD_FOLDER = str(Path(basedir, "apps", "images"))

class LocalConfig(BaseConfig):
    SQLALCHEMY_DARABASE_URI = f"sqlite:///{basedir/'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class TestingConfig(BaseConfig):
    SQLALCHEMY_DARABASE_URI = f"sqlite:///{basedir/'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

config ={
    "testing":TestingConfig,
    "local":LocalConfig,
}