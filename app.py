from flask import Flask, render_template, redirect, url_for, request, session, flash
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime

from models import (
    db,
    Worker,
    ProjectManager,
    Project,
    Attendance,
    WorkAssignment,
    WorkLog
)

from routes.project_routes import project_bp


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///construction_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db.init_app(app)

# Register Blueprints
app.register_blueprint(project_bp)


# ----------------------
# Public Routes
# ----------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------
# Admin Dashboard
# ----------------------
@app.route("/admin")
def admin_dashboard():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template("admin/dashboard.html", projects=projects)


# ----------------------
# Worker Dashboard
# ----------------------
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
# Worker Authentication
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


@app.route("/worker/login", methods=["GET", "POST"])
def worker_login():
    if request.method == "POST":
        worker = Worker.query.filter_by(email=request.form["email"]).first()
        if worker and worker.password == request.form["password"]:
            session["worker_id"] = worker.id
            return redirect(url_for("worker_dashboard"))

        flash("Invalid credentials", "error")

    return render_template("worker/login.html")


# ----------------------
# Worker Attendance & Logs
# ----------------------
@app.route("/worker/attendance", methods=["POST"])
def mark_attendance():
    attendance = Attendance(
        worker_id=session["worker_id"],
        status=request.form["status"]
    )
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for("worker_dashboard"))


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
# Project Manager Dashboard
# ----------------------
@app.route("/project-manager/dashboard")
def project_manager_dashboard():
    if "pm_id" not in session:
        return redirect(url_for("pm_login"))

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
# Approve / Reject Logs
# ----------------------
@app.route("/project-manager/work-log/<int:id>/approve", methods=["POST"])
def approve_work_log(id):
    log = WorkLog.query.get_or_404(id)
    log.status = "Approved"
    log.manager_comment = request.form.get("comment")
    db.session.commit()
    return redirect(url_for("project_manager_dashboard"))


@app.route("/project-manager/work-log/<int:id>/reject", methods=["POST"])
def reject_work_log(id):
    log = WorkLog.query.get_or_404(id)
    log.status = "Rejected"
    log.manager_comment = request.form.get("comment")
    db.session.commit()
    return redirect(url_for("project_manager_dashboard"))


# ----------------------
# Assign Work
# ----------------------
@app.route("/project-manager/assign-work", methods=["POST"])
def assign_work():
    due_date_str = request.form.get("due_date")
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

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
# Project Manager Auth
# ----------------------
@app.route("/project-manager/login", methods=["GET", "POST"])
def pm_login():
    if request.method == "POST":
        pm = ProjectManager.query.filter_by(email=request.form["email"]).first()

        if pm and pm.check_password(request.form["password"]):
            session.clear()            
            session["pm_id"] = pm.id
            session["pm_name"] = pm.name
            return redirect(url_for("project_manager_dashboard"))

        flash("Invalid email or password", "error")

    return render_template("project_manager/login.html")


@app.route("/project-manager/logout")
def pm_logout():
    session.clear()
    return redirect(url_for("pm_login"))


# ----------------------
# Admin: Create First PM
# ----------------------
@app.route("/admin/create-project-manager", methods=["GET", "POST"])
def create_project_manager():
    if request.method == "POST":
        email = request.form["email"]

        existing_pm = ProjectManager.query.filter_by(email=email).first()
        if existing_pm:
            flash("Project Manager with this email already exists", "error")
            return redirect(url_for("create_project_manager"))

        pm = ProjectManager(
            name=request.form["name"],
            email=email
        )
        pm.set_password(request.form["password"])

        db.session.add(pm)
        db.session.commit()

        flash("Project Manager created successfully", "success")
        return redirect(url_for("pm_login"))

    return render_template("admin/create_project_manager.html")


# ----------------------
# PM creates other PMs
# ----------------------
@app.route("/project-manager/create", methods=["POST"])
def pm_create_other_pm():
    #  Ensure Project Manager is logged in
    if "pm_id" not in session:
        flash("Please login first", "error")
        return redirect(url_for("pm_login"))

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    #  Basic form validation
    if not name or not email or not password:
        flash("All fields are required", "error")
        return redirect(url_for("project_manager_dashboard"))

    #  Prevent duplicate email BEFORE insert
    existing_pm = ProjectManager.query.filter_by(email=email).first()
    if existing_pm:
        flash("Project Manager with this email already exists", "error")
        return redirect(url_for("project_manager_dashboard"))

    #  Create new Project Manager
    pm = ProjectManager(name=name, email=email)
    pm.set_password(password)

    try:
        db.session.add(pm)
        db.session.commit()
        flash("New Project Manager created successfully", "success")

    except IntegrityError:
        db.session.rollback()
        flash("Email already exists", "error")

    return redirect(url_for("project_manager_dashboard"))



# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
