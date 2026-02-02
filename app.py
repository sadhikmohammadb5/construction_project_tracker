from flask import Flask, render_template, redirect, url_for, request, session, flash
from sqlalchemy.exc import IntegrityError

from datetime import date

from models.project_manager import ProjectManager
from routes.project_routes import project_bp

from flask import request, session
from models import db, Worker, Attendance, WorkLog

from models import Attendance, WorkLog, Worker, WorkAssignment

from datetime import datetime
from functools import wraps



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///construction_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db.init_app(app)

# Register Blueprints
app.register_blueprint(project_bp)


# ----------------------
# Dashboard Route
# ----------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin_dashboard():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template("admin/dashboard.html", projects=projects)


@app.route("/worker/dashboard")
def worker_dashboard():
    if "worker_id" not in session:
        return redirect(url_for("worker_login"))

    worker_id = session["worker_id"]

    assignments = WorkAssignment.query.filter_by(
        worker_id=worker_id
    ).order_by(WorkAssignment.created_at.desc()).all()

    attendance_marked = Attendance.query.filter_by(
        worker_id=worker_id,
        date=date.today()
    ).first()

    logs = WorkLog.query.filter_by(
        worker_id=worker_id
    ).order_by(WorkLog.created_at.desc()).all()

    return render_template(
    "worker/dashboard.html",
    assignments=assignments,
    attendance_marked=attendance_marked,
    logs=logs
)


# ----------------------
# Worker Authentication Routes
# ----------------------
@app.route("/worker/register", methods=["GET", "POST"])
def worker_register():
    if request.method == "POST":
        worker = Worker(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"]
        )

        try:
            db.session.add(worker)
            db.session.commit()
            return redirect(url_for("worker_login"))

        except IntegrityError:
            db.session.rollback()
            flash("Email already exists. Please login.", "error")
            return redirect(url_for("worker_register"))

    return render_template("worker/register.html")
# ----------------------
# Worker Login Route


@app.route("/worker/login", methods=["GET", "POST"])
def worker_login():
    if request.method == "POST":
        worker = Worker.query.filter_by(email=request.form["email"]).first()
        if worker and worker.password == request.form["password"]:
            session["worker_id"] = worker.id
            return redirect(url_for("worker_dashboard"))

    return render_template("worker/login.html")

# ----------------------
# Worker Attendance and Work Log Routes

@app.route("/worker/attendance", methods=["POST"])
def mark_attendance():
    attendance = Attendance(
        worker_id=session["worker_id"],
        status=request.form["status"]
    )
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for("worker_dashboard"))


# ----------------------
# Worker Work Log Route

@app.route("/worker/work-log", methods=["POST"])
def submit_work_log():
    log = WorkLog(
        worker_id=session["worker_id"],
        description=request.form["description"],
        hours_worked=request.form["hours"]
    )
    db.session.add(log)
    db.session.commit()
    return redirect(url_for("worker_dashboard"))

# ----------------------
# Project Manager Dashboard Route
# ----------------------

@app.route("/project-manager/dashboard")
def project_manager_dashboard():
    attendances = Attendance.query.order_by(Attendance.date.desc()).all()
    work_logs = WorkLog.query.order_by(WorkLog.created_at.desc()).all()
    workers = Worker.query.all()

    return render_template(
        "project_manager/dashboard.html",
        attendances=attendances,
            work_logs=work_logs,
            workers=workers
        )

    
# ----------------------
# Approve Work Log Route
# ----------------------

@app.route("/project-manager/work-log/<int:id>/approve", methods=["POST"])
def approve_work_log(id):
    log = WorkLog.query.get_or_404(id)
    log.status = "Approved"
    log.manager_comment = request.form.get("comment")
    db.session.commit()
    return redirect(url_for("project_manager_dashboard"))

# ----------------------
# Reject Work Log Route
# ----------------------

@app.route("/project-manager/work-log/<int:id>/reject", methods=["POST"])
def reject_work_log(id):
    log = WorkLog.query.get_or_404(id)
    log.status = "Rejected"
    log.manager_comment = request.form.get("comment")
    db.session.commit()
    return redirect(url_for("project_manager_dashboard"))

# ----------------------
# Assign Work Route
# ----------------------



@app.route("/project-manager/assign-work", methods=["POST"])
def assign_work():
    due_date_str = request.form.get("due_date")

    due_date = (
        datetime.strptime(due_date_str, "%Y-%m-%d").date()
        if due_date_str else None
    )

    assignment = WorkAssignment(
        worker_id=request.form["worker_id"],
        project_id=request.form.get("project_id"),
        task_title=request.form["task_title"],
        instructions=request.form["instructions"],
        due_date=due_date
    )

    db.session.add(assignment)
    db.session.commit()

    return redirect(url_for("project_manager_dashboard"))

# ----------------------
# Project Manager Login Route
# ----------------------

@app.route("/project-manager/login", methods=["GET", "POST"])
def pm_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        pm = ProjectManager.query.filter_by(email=email).first()

        if pm and pm.check_password(password):
            session["pm_id"] = pm.id
            session["pm_name"] = pm.name
            return redirect(url_for("project_manager_dashboard"))

        flash("Invalid email or password", "error")

    return render_template("project_manager/login.html")


# ----------------------    
# Project Manager Logout Route
# ----------------------    

@app.route("/project-manager/logout")
def pm_logout():
    session.clear()
    return redirect(url_for("pm_login"))

# ----------------------
# Create Project Manager Route
# ----------------------
@app.route("/admin/create-project-manager", methods=["GET", "POST"])
def create_project_manager():
    if request.method == "POST":
        pm = ProjectManager(
            name=request.form["name"],
            email=request.form["email"]
        )
        pm.set_password(request.form["password"])

        db.session.add(pm)
        db.session.commit()

        flash("Project Manager created successfully", "success")
        return redirect(url_for("pm_login"))

    return render_template("admin/create_project_manager.html")

# ----------------------
@app.route("/project-manager/create", methods=["POST"])
def pm_create_other_pm():
    pm = ProjectManager(
        name=request.form["name"],
        email=request.form["email"]
    )
    pm.set_password(request.form["password"])

    db.session.add(pm)
    db.session.commit()

    flash("New Project Manager created", "success")
    return redirect(url_for("project_manager_dashboard"))


# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
