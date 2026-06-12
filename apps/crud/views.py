from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for

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
    form = UserForm()



    user = User.query.filter_by(id=user_id).first()



    if form.validate_on_submit():
        user.username = form.email.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_template("crud/edit.html", user=user, form=form)
