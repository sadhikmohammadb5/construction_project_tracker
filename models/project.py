from datetime import datetime
from models import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200))
    client = db.Column(db.String(150))
    manager = db.Column(db.String(150))

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default="On Track")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="project", lazy=True)
    budgets = db.relationship("Budget", backref="project", lazy=True)
    issues = db.relationship("Issue", backref="project", lazy=True)
    daily_logs = db.relationship("DailyLog", backref="project", lazy=True)

    def __repr__(self):
        return f"<Project {self.name}>"
