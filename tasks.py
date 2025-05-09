from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Task, Goal

tasks_bp = Blueprint('tasks', __name__)

# Просмотр всех задач
@tasks_bp.route('/tasks')
@login_required
def list_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

# Создание новой задачи
@tasks_bp.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        name = request.form['name']
        progress = int(request.form['progress'])
        goal_id = int(request.form['goal_id'])
        task = Task(name=name, progress=progress, goal_id=goal_id, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.list_tasks'))
    return render_template('new_task.html', goals=goals)

# Редактирование задачи
@tasks_bp.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return "Недостаточно прав", 403

    goals = Goal.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        task.name = request.form['name']
        task.progress = int(request.form['progress'])
        task.goal_id = int(request.form['goal_id'])
        db.session.commit()
        return redirect(url_for('tasks.list_tasks'))

    return render_template('edit_task.html', task=task, goals=goals)
