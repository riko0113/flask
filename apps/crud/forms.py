from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名は必須です。"),
            Length(max=30, message="30文字以内で入力してください。"),
        ],
    )

    birthday = DateField(
        "生年月日",
        validators=[DataRequired(message="生年月日は必須です。")],
        format='%Y-%m-%d'  # HTMLの <input type="date"> と合わせる設定
    )

    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(messages="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[DataRequired(messages="パスワードは必須です。")]
    )

    submit = SubmitField("新規登録")