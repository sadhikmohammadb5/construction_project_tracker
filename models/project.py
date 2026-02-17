from datetime import datetime
from models import db

from . import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    budget = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(50), default="On Track")
    
    assignment_status = db.Column(db.String(50), default="Pending")


    project_manager_id = db.Column(
        db.Integer,
        db.ForeignKey("project_managers.id"),
        nullable=True
    )

    project_manager = db.relationship(
        "ProjectManager",
        backref="projects"
    )
