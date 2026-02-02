from datetime import date
from . import db

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    worker_id = db.Column(
        db.Integer,
        db.ForeignKey("workers.id"),  # ✅ FIXED
        nullable=False
    )

    date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), nullable=False)

    worker = db.relationship("Worker", backref="attendance")
