from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired

from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UplodImageForm(FlaskForm):

    image = FileField(
        "画像",
        validators=[
            FileRequired("画像ファイルを指定してください。"),
            FileAllowed(
                ["png", "jpg", "jpeg"],
                "サポートされていない画像形式です。"
            ),
        ]
    )

    genre = SelectField(
        "ジャンル",
        choices=[
            ("animal", "動物"),
            ("food", "食べ物"),
            ("game", "ゲーム"),
            ("other", "その他"),
        ],
        validators=[DataRequired()]
    )

    comment = TextAreaField(
        "コメント",
        validators=[DataRequired()]
    )

    submit = SubmitField("アップロード")


# 編集用フォーム
class EditForm(FlaskForm):
    image = FileField(
        "画像",
        validators=[
            FileRequired("画像ファイルを指定してください。"),
            FileAllowed(
                ["png", "jpg", "jpeg"],
                "サポートされていない画像形式です。"
            ),
        ]
    )

    genre = SelectField(
        "ジャンル",
        choices=[
            ("animal", "動物"),
            ("food", "食べ物"),
            ("drink", "飲み物"),
            ("game", "ゲーム"),
            ("other", "その他"),
        ],
        validators=[DataRequired()]
    )

    comment = TextAreaField(
        "コメント",
        validators=[DataRequired()]
    )

    submit = SubmitField("更新")


class DeleteForm(FlaskForm):
    submit = SubmitField("削除")