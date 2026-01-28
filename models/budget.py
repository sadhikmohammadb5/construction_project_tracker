from datetime import datetime
from models import db

class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    category = db.Column(db.String(100), nullable=False)
    budgeted = db.Column(db.Float, nullable=False)
    actual = db.Column(db.Float, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def variance(self):
        return self.budgeted - self.actual

    def __repr__(self):
        return f"<Budget {self.category}>"
