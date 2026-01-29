from models import db
from datetime import date

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("workers.id"))
    date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20))  # Present / Absent
