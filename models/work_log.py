from models import db
from datetime import date

class WorkLog(db.Model):
    __tablename__ = "work_logs"

    id = db.Column(db.Integer, primary_key=True)

    worker_id = db.Column(
        db.Integer,
        db.ForeignKey("workers.id"),
        nullable=False
    )

    description = db.Column(db.Text, nullable=False)
    hours_worked = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    manager_comment = db.Column(db.Text)

    created_at = db.Column(
        db.Date,
        default=date.today
    )

    worker = db.relationship("Worker", backref="work_logs")
