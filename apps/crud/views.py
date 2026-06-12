from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for
from flask import abort
from flask_login import current_user, login_required

crud= Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/users/new", methods=["GET","POST"])
def create_user():
    form = UserForm()

    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            birthday=form.birthday.data,
        )

        try:
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("crud.users"))

        except ValueError as e:
            db.session.rollback()
            form.birthday.errors.append(str(e))

    return render_template("crud/create.html, form=form")

@crud.route("/users/<user_id>", methods=["GET","POST"])
def edit_user(user_id):
<<<<<<< HEAD
    form = UserForm()
=======
    if int(user_id) != current_user.id:
        abort(403)
>>>>>>> 5c14cc7a134cabeec60045162f75567d3d28f4bf

    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)

<<<<<<< HEAD
=======
    form = UserForm()

    if request.method == "GET":
        form.username.data = user.username
        form.email.data = user.email

>>>>>>> 5c14cc7a134cabeec60045162f75567d3d28f4bf
    if form.validate_on_submit():
        user.username = form.email.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_template("crud/edit.html", user=user, form=form)