from datetime import datetime
from models import db

class DailyLog(db.Model):
    __tablename__ = "daily_logs"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    date = db.Column(db.Date, default=datetime.utcnow)
    weather = db.Column(db.String(100))
    crew_size = db.Column(db.Integer)

    work_done = db.Column(db.Text)
    issues = db.Column(db.Text)
    safety_notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DailyLog {self.date}>"
