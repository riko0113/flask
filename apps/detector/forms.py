from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms import TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields.simple import SubmitField


# 新規投稿
class UploadImageForm(FlaskForm):
    image = FileField(
        "画像",
        validators=[
            FileRequired("おすすめのお酒の画像を入れてください♪"),
            FileAllowed(["png", "jpg", "jpeg"],
            "サポートされていない画像形式です。"),
        ]
    )

    genre = SelectField(
        "ジャンル",
        choices=[
            ("日本酒", "日本酒"),
            ("ビール", "ビール"),
            ("ワイン", "ワイン"),
            ("ウイスキー", "ウイスキー"),
            ("カクテル", "カクテル"),
            ("チューハイ", "チューハイ"),
            ("その他", "その他"),
        ],
        validators=[
            DataRequired()
        ],
    )
    
    comment = TextAreaField(
        "コメント",
        validators=[
            DataRequired(message="コメントを入力してください♬"),
            Length(max=300, message="コメントは300文字以内で入力してください。"),
        ],
    )

    submit = SubmitField("アップロード")


# 編集用フォーム
class EditForm(FlaskForm):
    image = FileField(
        "画像",
        validators=[
            FileRequired("おすすめのお酒の画像を入れてください♪"),
            FileAllowed(["png", "jpg", "jpeg"],
            "サポートされていない画像形式です。"),
        ]
    )

    genre = SelectField(
        "ジャンル",
        choices=[
            ("日本酒", "日本酒"),
            ("ビール", "ビール"),
            ("ワイン", "ワイン"),
            ("ウイスキー", "ウイスキー"),
            ("カクテル", "カクテル"),
            ("チューハイ", "チューハイ"),
            ("おつまみ", "おつまみ"),
            ("その他", "その他"),
        ],
        validators=[
            DataRequired()
        ],
    )
    
    comment = TextAreaField(
        "コメント",
        validators=[
            DataRequired(message="コメントを入力してください♬"),
            Length(max=300, message="コメントは300文字以内で入力してください。"),
        ],
    )

    submit = SubmitField("更新")


class DeleteForm(FlaskForm):
    submit = SubmitField("削除")