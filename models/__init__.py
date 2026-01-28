from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .project import Project
from .task import Task
from .budget import Budget
from .daily_log import DailyLog
from .issue import Issue

