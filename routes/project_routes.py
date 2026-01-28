from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Project

project_bp = Blueprint("projects", __name__)


# ----------------------
# List Projects
# ----------------------
@project_bp.route("/projects")
def list_projects():
    projects = Project.query.all()
    return render_template("projects/list.html", projects=projects)


# ----------------------
# Create Project
# ----------------------
@project_bp.route("/projects/new", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        project = Project(
            name=request.form["name"],
            location=request.form["location"],
            client=request.form["client"],
            manager=request.form["manager"],
            status=request.form["status"]
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("projects.list_projects"))

    return render_template("projects/create.html")


# ----------------------
# Project Detail
# ----------------------
@project_bp.route("/projects/<int:id>")
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template("projects/detail.html", project=project)


# ----------------------
# Edit Project
# ----------------------
@project_bp.route("/projects/<int:id>/edit", methods=["GET", "POST"])
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == "POST":
        project.name = request.form["name"]
        project.location = request.form["location"]
        project.client = request.form["client"]
        project.manager = request.form["manager"]
        project.status = request.form["status"]

        db.session.commit()
        return redirect(url_for("projects.project_detail", id=id))

    return render_template("projects/edit.html", project=project)


# ----------------------
# Delete Project
# ----------------------
@project_bp.route("/projects/<int:id>/delete", methods=["POST"])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("projects.list_projects"))
