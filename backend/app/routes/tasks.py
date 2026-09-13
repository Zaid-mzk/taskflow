from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Task, Project

tasks_bp = Blueprint("tasks", __name__)

VALID_STATUSES = {"todo", "in_progress", "done"}


def _get_owned_task(task_id, user_id):
    task = db.session.get(Task, task_id)
    if not task:
        return None
    project = Project.query.filter_by(id=task.project_id, owner_id=user_id).first()
    if not project:
        return None
    return task


@tasks_bp.route("/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = _get_owned_task(task_id, user_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({"error": "Invalid status"}), 400
        task.status = data["status"]
    if "title" in data:
        if not data["title"].strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        task.title = data["title"].strip()
    if "description" in data:
        task.description = data["description"]
    if "due_date" in data:
        if data["due_date"]:
            try:
                task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "due_date must be in YYYY-MM-DD format"}), 400
        else:
            task.due_date = None

    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = _get_owned_task(task_id, user_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
