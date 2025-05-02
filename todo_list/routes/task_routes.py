from flask import Blueprint, jsonify, request, abort
from models.models_task import Task
from database import Database
from flask_jwt_extended import jwt_required


class TaskRoutes:
    """
    A class to manage routes for the task-related API endpoints in the Flask application.

    Attributes:
        app (Flask): The Flask app instance.
        db (Database): The database connection object.
        task_bp (Blueprint): The Flask blueprint to handle task-related routes.
    """
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.task_bp = Blueprint('task_bp', __name__)
        self.register_routes()

    def register_routes(self):
        self.task_bp.route('/tasks', methods=['GET'])(self.get_tasks)
        self.task_bp.route('/tasks/<int:task_id>', methods=['GET'])(self.get_task)
        self.task_bp.route('/tasks', methods=['POST'])(self.create_task)
        self.task_bp.route('/tasks/<int:task_id>', methods=['PUT'])(self.update_task)
        self.task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])(self.delete_task)
        self.app.register_blueprint(self.task_bp)

    @jwt_required()
    def get_tasks(self):
        tasks = Task.get_all(db=self.db)
        return jsonify([{
            'id': task.id,
            'title': task.title,
            'description': task.description
        } for task in tasks]), 200

    @jwt_required()
    def get_task(self, task_id):
        try:
            task = Task.get_by_id(task_id, db=self.db)
        except Exception as e:
            if 'Task not found' in str(e):
                abort(404, description='Task not found')
            raise
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description
        }), 200

    @jwt_required()
    def create_task(self):
        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()

        errors = []
        if not title or len(title) < 3:
            errors.append('Title must be at least 3 characters long.')
        if description and len(description) > 255:
            errors.append('Description must be less than 255 characters.')

        if errors:
            return jsonify({'errors': errors}), 400

        task = Task(title=title, description=description, db=self.db)
        task.save()
        return jsonify({'message': 'Task created successfully'}), 201

    @jwt_required()
    def update_task(self, task_id):
        try:
            task = Task.get_by_id(task_id, db=self.db)
        except Exception as e:
            if 'Task not found' in str(e):
                abort(404, description='Task not found')
            raise

        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()

        errors = []
        if not title or len(title) < 3:
            errors.append('Title must be at least 3 characters long.')
        if description and len(description) > 255:
            errors.append('Description must be less than 255 characters.')

        if errors:
            return jsonify({'errors': errors}), 400

        task.title = title
        task.description = description
        task.update()
        return jsonify({'message': 'Task updated successfully'}), 200

    @jwt_required()
    def delete_task(self, task_id):
        try:
            Task.get_by_id(task_id, db=self.db)
        except Exception as e:
            if 'Task not found' in str(e):
                abort(404, description='Task not found')
            raise

        Task.delete(task_id, db=self.db)
        return jsonify({'message': 'Task deleted successfully'}), 200