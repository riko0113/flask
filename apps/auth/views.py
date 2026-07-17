from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder=""
)

@auth.route("/")
def index():
    return render_template("auth/index.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            birthday=form.birthday.data,
            email=form.email.data,
            password=form.password.data,
        )

        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))

        db.session.add(user)
        db.session.commit()

        flash("登録が完了しました。ログインしてください。")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("face.index"))
        
        flash("メールアドレスかパスワードが不正です")
    return render_template("auth/login.html", form=form)

@auth.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("ログアウトしました")
    return redirect(url_for("auth.login"))