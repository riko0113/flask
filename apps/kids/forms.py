from flask_wtf.file import FileAllowed,FileField,FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField

class UplodImageForm(FlaskForm):
    image = FileField(
        validators=[
            FileRequired("画像ファイルを指定してください。"),
            FileAllowed(["png","jpg","jpeg"],
            "サポートされていない画像形式です。"),
        ]
    )

    submit = SubmitField("アップロード")

class DeleteForm(FlaskForm):
    submit = SubmitField("削除")