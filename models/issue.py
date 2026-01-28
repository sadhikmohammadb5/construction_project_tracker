from datetime import datetime
from models import db

class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    ref_type = db.Column(db.String(20))  # Issue / RFI / CO
    description = db.Column(db.Text, nullable=False)
    impact = db.Column(db.String(50))    # Cost / Schedule / Both

    status = db.Column(db.String(30), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Issue {self.ref_type} {self.id}>"
