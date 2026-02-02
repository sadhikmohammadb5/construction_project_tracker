from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .worker import Worker
from .project_manager import ProjectManager
from .project import Project
from .task import Task
from .attendance import Attendance
from .work_assignment import WorkAssignment
from .work_log import WorkLog
