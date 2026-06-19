from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for
from flask import abort
from flask_login import current_user, login_required

face= Blueprint(
    "face",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@face.route("/")
@login_required
def index():
    return render_template("face/snipet.html")
