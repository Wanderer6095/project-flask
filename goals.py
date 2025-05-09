from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Goal

goals_bp = Blueprint('goals', __name__)

# Просмотр списка целей
@goals_bp.route('/goals')
@login_required
def list_goals():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals.html', goals=goals)

# Создание новой цели
@goals_bp.route('/goals/new', methods=['GET', 'POST'])
@login_required
def new_goal():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        goal = Goal(title=title, description=description, user_id=current_user.id)
        db.session.add(goal)
        db.session.commit()
        return redirect(url_for('goals.list_goals'))
    return render_template('new_goal.html')

# Редактирование цели
@goals_bp.route('/goals/edit/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        return "Недостаточно прав", 403
    if request.method == 'POST':
        goal.title = request.form['title']
        goal.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('goals.list_goals'))
    return render_template('edit_goal.html', goal=goal)
