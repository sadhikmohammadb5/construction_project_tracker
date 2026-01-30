from models import db
from datetime import datetime

class WorkAssignment(db.Model):
    __tablename__ = "work_assignments"

    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("workers.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    task_title = db.Column(db.String(200))
    instructions = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
