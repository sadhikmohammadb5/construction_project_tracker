from models import db
from datetime import datetime

class WorkLog(db.Model):
    __tablename__ = "work_logs"

    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("workers.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)

    description = db.Column(db.Text, nullable=False)
    hours_worked = db.Column(db.Integer)

    status = db.Column(db.String(20), default="Pending")  # Pending / Approved / Rejected
    manager_comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
