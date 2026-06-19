from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm
from apps.crud.models import User
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask import abort
from flask_login import current_user, login_required

crud= Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/users/new", methods=["GET","POST"])
@login_required
def create_user():
    form = UserForm()

    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            birthday=form.birthday.data,
            email=form.email.data,
            password=form.password.data,
        )

        try:
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("auth.login"))

        except ValueError as e:
            db.session.rollback()
            form.birthday.errors.append(str(e))

    return render_template("crud/create.html", form=form)

@crud.route("/users/<user_id>", methods=["GET","POST"])
@login_required
def edit_user(user_id):
    if int(user_id) != current_user.id:
        abort(403)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)

    form = UserForm()

    if request.method == "GET":
        form.username.data = user.username
        form.email.data = user.email

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))

@crud.route("/verify_age", methods=["POST"])
@login_required
def verify_age():
    data = request.get_json()
    if not data or "camera_age" not in data:
        return jsonify({"status": "error", "message": "データが不足しています"}), 400

    camera_age = round(data["camera_age"])  # カメラが予測した年齢
    real_age = current_user.age             # 💡 あなたが作ったモデルの age プロパティを利用！

    if real_age is None:
        return jsonify({"status": "error", "message": "誕生日が登録されていません"}), 400

    # 💡 【照合ロジック】誤差±5歳以内なら本人と判定
    age_difference = abs(camera_age - real_age)
    
    if age_difference <= 5:
        return jsonify({
            "status": "success", 
            "match": True, 
            "redirect_url": url_for("detector.index")  # ★成功時の遷移先URL
        })
    else:
        return jsonify({
            "status": "success", 
            "match": False, 
            "redirect_url": url_for("detector.index")   # ★失敗時の遷移先URL
        })
