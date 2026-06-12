import uuid
from pathlib import Path
from apps.app import SQLALCHEMY_DARABASE_URI
from apps.crud.models import User
from apps.detector.models import UserImage
from apps.detector.forms import UploadImageFrom
from flask import (
    Blueprint,
    current_app,
    render_template,
    send_from_directory,
    redirect,
    url_for,
)
from flask_login import current_user, login_required


dt = Blueprint("detector", __name__, template_folder="templates")

@dt.route("/")
def index():
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )

    return render_template("detector/index.html", user_images=user_images)

@dt.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@dt.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
    form = UploadImageFrom()
    if form.valudate_on_submit():
        file = form.image.data
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid4.uuid4()) + ext

        image_path = Path(
            current_app.config["UPLOAD_FOVDER"], image_uuid_file_name
        )
        file.save()

        user_image = UserImage(
            user_id=current_user.id, image_path=image_uuid_file_name
        )
        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("detector.index"))
    return render_template("detctor/upload.html", form=form)