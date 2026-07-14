import uuid
from pathlib import Path
from sqlalchemy import or_

from flask import (
    Blueprint,
    current_app,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    request,
)

from flask_login import current_user, login_required

from apps.app import db
from apps.crud.models import User
from apps.kids.models import KidsImage
from apps.kids.forms import UplodImageForm, DeleteForm, EditForm
from apps.kids.image_check import check_ng_image


kids = Blueprint("kids", __name__, template_folder="templates")


@kids.route("/")
def index():
    user_images = (
        db.session.query(User, KidsImage)
        .join(KidsImage)
        .filter(User.id == KidsImage.user_id)
        .all()
    )
    
    delete_form = DeleteForm()

    return render_template("kids/index.html", user_images=user_images, delete_form=delete_form)


@kids.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )


@kids.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
    form = UplodImageForm()

    if form.validate_on_submit():
        file = form.image.data
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        image_path = Path(
            current_app.config["UPLOAD_FOLDER"],
            image_uuid_file_name
        )
        # 画像を一時保存
        file.save(image_path)

        # AIチェック
        is_ng, reason, score = check_ng_image(image_path)
        if is_ng and score > 0.47:
            # 保存した画像を削除
            image_path.unlink()
            form.image.errors.append(
                f"これは{reason}のため投稿できません。"
            )
            return render_template(
                "kids/upload.html",
                form=form
            )

        # 問題なければDBに保存
        user_image = KidsImage(
            user_id=current_user.id,
            image_path=image_uuid_file_name,
            genre=form.genre.data,        
            comment=form.comment.data,
            is_detected=True,
            detection_reason="問題なし"   
        )

        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("kids.index"))

    return render_template("kids/upload.html", form=form)

@kids.route("/delete/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    image = KidsImage.query.get_or_404(image_id)

    if str(image.user_id) != str(current_user.id):
        return redirect(url_for("kids.index"))

    db.session.delete(image)
    db.session.commit()

    return redirect(url_for("kids.index"))

@kids.route("/user/<int:user_id>/posts")
@login_required
def account(user_id):
    selected_user = User.query.get_or_404(user_id)
    
    user_images = db.session.query(User, KidsImage).join(
        KidsImage, User.id == KidsImage.user_id
    ).filter(User.id == user_id).all()
    
    return render_template(
        "kids/account.html",
        selected_user=selected_user,
        user_images=user_images
    )
    
@kids.route("/edit/<int:image_id>", methods=["GET", "POST"])
@login_required
def edit_image(image_id):
    image = KidsImage.query.get_or_404(image_id)

    # 自分の投稿だけ編集可能
    if str(image.user_id) != str(current_user.id):
        return redirect(url_for("kids.index"))
    form = EditForm(obj=image)

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
             # AIチェック
            is_ng, reason, score = check_ng_image(image_path)

            if is_ng and score > 0.35:
                # 禁止画像なので削除
                if image_path.exists():
                    image_path.unlink()

                form.image.errors.append(
                    f"これは{reason}のため変更できません。"
                )
                return render_template(
                    "kids/edit.html",
                    form=form,
                    image=image
                )
            
            # 問題なければ画像を変更
            old_image_path = Path(
                current_app.config["UPLOAD_FOLDER"],
                image.image_path
            )
            # 古い画像を削除
            if old_image_path.exists():
                old_image_path.unlink()

            image.image_path = filename
            image.is_detected = True
            image.detection_reason = "問題なし"

        db.session.commit()
        return redirect(url_for("kids.index"))

    return render_template("kids/edit.html", form=form,  image=image)

@kids.route("/search", methods=["GET"])
@login_required
def search():
    # 1. リクエストから検索ワードを取得
    search_text = request.args.get("search")

    # 2. 基本となるクエリ（UserとUserImageを結合）
    query = db.session.query(User, KidsImage).join(
        KidsImage, User.id == KidsImage.user_id
    )

    # 3. 検索ワードがある場合、ジャンルまたはコメントでフィルタリング
    if search_text:
        like_text = f"%{search_text}%"
        query = query.filter(
            or_(
                KidsImage.genre.like(like_text),     # ジャンルに部分一致
                KidsImage.comment.like(like_text)     # コメントに部分一致
            )
        )

    # クエリの実行（絞り込まれた結果をリストで取得）
    filtered_user_images = query.all()

    # 4. 画面に必要なフォームの用意
    delete_form = DeleteForm()

    # 5. テンプレートへ渡す
    return render_template(
        "kids/index.html",
        user_images=filtered_user_images,
        delete_form=delete_form,
    )