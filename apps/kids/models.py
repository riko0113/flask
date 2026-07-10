from datetime import datetime 

from apps.app import db 

class KidsImage(db.Model):
    __tablename__ = "kids_images"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    image_path = db.Column(db.String)
    is_detected = db.Column(db.Boolean, default=False)
    detection_reason = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    genre = db.Column(db.String(50))
    comment = db.Column(db.Text)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )