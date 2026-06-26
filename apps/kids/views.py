import uuid
from apps.app import db
from apps.crud.models import User
from pathlib import Path
from apps.kids.models import KidsImage
from apps.kids.forms import UplodImageForm
from flask import (
    Blueprint,
    current_app,
    render_template,
    send_from_directory,
    redirect,
    url_for,
)

from flask_login import current_user, login_required

kids= Blueprint("kids", __name__, template_folder="templates")

@kids.route("/")
def index():
    user_images= (

        db.session.query(User, KidsImage)
        .join(KidsImage)
        .filter(User.id == KidsImage.user_id)
        .all()
    )
    return render_template("Kids/index.html", user_images=user_images)

@kids.route("/images/<path:filanme>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"],filename)

@kids.route("/upload",methods =["GET","POST"])
@login_required
def upload_image():
    form = UplodImageForm()

    if form.validate_on_submit():
        file = form.image.data
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        image_path = Path(
            current_app.config["UPLOAD_FOLDER"],image_uuid_file_name
        )
        file.save(image_path)

        user_image=KidsImage(
            user_id = current_user.id,image_path=image_uuid_file_name
        )
        db.session.add(user_image)
        db.session.commit()


        return redirect(url_for("kids.index"))
    return render_template("kids/upload.html",form=form)