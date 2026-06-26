from apps.app import db
from apps.crud.models import User

from apps.kids.models import KidsImage
from flask import Blueprint, render_template
#あああ

dt = Blueprint(
    "kids",
    __name__,
    template_folder="templates",
)

@dt.route("/")
def index():
    user_images= (

        db.session.query(User, KidsImage)
        .join(KidsImage)
        .filter(User.id == KidsImage.user_id)
        .all()
    )
    return render_template("Kids/index.html", user_images=user_images)