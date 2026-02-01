from models import db
from datetime import datetime

class WorkAssignment(db.Model):
    __tablename__ = "work_assignments"

    id = db.Column(db.Integer, primary_key=True)

    worker_id = db.Column(db.Integer, db.ForeignKey("workers.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)

    task_title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(50), default="Assigned")
    due_date = db.Column(db.Date)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    worker = db.relationship("Worker", backref="assignments")
    project = db.relationship("Project", backref="assignments")
