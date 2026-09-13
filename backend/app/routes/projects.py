from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Project, Task

projects_bp = Blueprint("projects", __name__)

VALID_STATUSES = {"todo", "in_progress", "done"}


@projects_bp.route("", methods=["GET"])
@jwt_required()
def list_projects():
    user_id = int(get_jwt_identity())
    projects = Project.query.filter_by(owner_id=user_id).order_by(Project.created_at.desc()).all()
    return jsonify([p.to_dict(include_task_counts=True) for p in projects]), 200


@projects_bp.route("", methods=["POST"])
@jwt_required()
def create_project():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Project name is required"}), 400

    project = Project(name=name, description=description, owner_id=user_id)
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201


@projects_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
def get_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project.to_dict(include_task_counts=True)), 200


@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"}), 200


@projects_bp.route("/<int:project_id>/tasks", methods=["GET"])
@jwt_required()
def list_tasks(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    status_filter = request.args.get("status")
    query = Task.query.filter_by(project_id=project_id)
    if status_filter:
        if status_filter not in VALID_STATUSES:
            return jsonify({"error": "Invalid status filter"}), 400
        query = query.filter_by(status=status_filter)

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@projects_bp.route("/<int:project_id>/tasks", methods=["POST"])
@jwt_required()
def create_task(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "due_date must be in YYYY-MM-DD format"}), 400

    task = Task(
        project_id=project_id,
        title=title,
        description=data.get("description", ""),
        due_date=due_date,
        status=data.get("status", "todo") if data.get("status") in VALID_STATUSES else "todo",
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201
