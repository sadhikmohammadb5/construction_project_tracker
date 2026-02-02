from datetime import datetime
from models import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
   
    def __repr__(self):
        return f"<Project {self.name}>"
