import uuid
from pathlib import Path
from apps.app import db
from apps.crud.models import User
from apps.detector.models import UserImage
from apps.detector.forms import UploadImageForm, DeleteForm, EditForm
from flask import (
    Blueprint,
    current_app,
    render_template,
    send_from_directory,
    redirect,
    url_for,
)
from flask_login import current_user, login_required


detector = Blueprint("detector", __name__, template_folder="templates")

@detector.route("/")
@login_required
def index():
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage, User.id == UserImage.user_id)
        .filter(User.id == current_user.id)
        .all()
    )

    delete_form = DeleteForm()

    return render_template(
        "detector/index.html",
        user_images=user_images,
        delete_form=delete_form
    )

@detector.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@detector.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        image_path = Path(
            current_app.config["UPLOAD_FOLDER"], image_uuid_file_name
        )
        file.save(image_path)

        user_image = UserImage(
            user_id=current_user.id,
            image_path=image_uuid_file_name,
            genre=form.genre.data,
            comment=form.comment.data
        )
        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("detector.index"))
    return render_template("detector/upload.html", form=form)

@detector.route("/delete/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    image = UserImage.query.get_or_404(image_id)

    if str(image.user_id) != str(current_user.id):
        return redirect(url_for("detector.index"))

    db.session.delete(image)
    db.session.commit()

    return redirect(url_for("detector.index"))

@detector.route("/user/<int:user_id>/posts")
@login_required
def account(user_id):
    selected_user = User.query.get_or_404(user_id)
    
    user_images = db.session.query(User, UserImage).join(
        UserImage, User.id == UserImage.user_id
    ).filter(User.id == user_id).all()
    
    return render_template(
        "detector/account.html",
        selected_user=selected_user,
        user_images=user_images
    )
    
@detector.route("/edit/<int:image_id>", methods=["GET", "POST"])
@login_required
def edit_image(image_id):
    image = UserImage.query.get_or_404(image_id)

    # 自分の投稿だけ編集可能
    if image.user_id != current_user.id:
        return redirect(url_for("detector.index"))
    form = EditImageForm(obj=image)

    if form.validate_on_submit():
        # ジャンル・コメントを更新
        image.genre = form.genre.data
        image.comment = form.comment.data
        # 画像が選択された場合のみ更新
        if form.image.data:
            file = form.image.data
            ext = Path(file.filename).suffix
            filename = str(uuid.uuid4()) + ext
            image_path = Path(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            file.save(image_path)
            image.image_path = filename

        db.session.commit()
        return redirect(url_for("detector.index"))

    return render_template("detector/edit.html", form=form,  image=image)
