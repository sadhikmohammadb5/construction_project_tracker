from models import db
from datetime import date

class WorkAssignment(db.Model):
    __tablename__ = "work_assignments"

    id = db.Column(db.Integer, primary_key=True)

    worker_id = db.Column(
        db.Integer,
        db.ForeignKey("workers.id"),
        nullable=False
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=True
    )

    task_title = db.Column(db.String(150), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    due_date = db.Column(db.Date, nullable=True)

    status = db.Column(
        db.String(20),
        default="Assigned"
    )

    created_at = db.Column(
        db.Date,
        default=date.today
    )

    worker = db.relationship("Worker", backref="assignments")
    project = db.relationship("Project", backref="assignments")
