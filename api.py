from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import Task, Goal

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/tasks')
@login_required
def api_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': t.id, 'name': t.name, 'progress': t.progress} for t in tasks])

@api_bp.route('/api/goals')
@login_required
def api_goals():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': g.id, 'title': g.title} for g in goals])
