from flask import Flask, redirect, render_template, url_for
from datetime import date

from models import db, Project, Task, Issue
from routes.project_routes import project_bp

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


@app.route("/project-manager")
def project_manager_dashboard():
    return render_template("project_manager/dashboard.html")


@app.route("/worker")
def worker_dashboard():
    return render_template("worker/dashboard.html")



# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
