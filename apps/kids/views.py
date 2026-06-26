from apps.app import db
from apps.crud.models import User

from apps.Kids.models import KidsImage
from flask import Blueprint, render_template
#あああ

dt = Blueprint(
    "Kids",
    __name__,
    template_folder="templates",
)

@dt.route("/")
def index():
    user_images= (
<<<<<<< HEAD
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
=======
        db.session.query(User, KidsImage)
        .join(KidsImage)
        .filter(User.id == KidsImage.user_id)
>>>>>>> 913597f45fa8709d12565f0ea017fff4112d83ee
        .all()
    )
    return render_template("Kids/index.html", user_images=user_images)