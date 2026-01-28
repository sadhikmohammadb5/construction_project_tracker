from datetime import datetime
from models import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    name = db.Column(db.String(200), nullable=False)
    phase = db.Column(db.String(100))

    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)

    status = db.Column(db.String(20), default="Pending")
    progress = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.name}>"
