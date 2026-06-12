from datetime import datetime, date
from apps.app import db
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import validates


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    birthday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #生年月日が未来の日付ではないかチェック
    @validates('birthday')
    def validate_birthday(self, key, value):
        if value > date.today():
            raise ValueError("生年月日に未来の日付は設定できません。")
        return value

    #年齢を計算
    @property
    def age(self):
        if not self.birthday:
            return None
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))