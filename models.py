from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)  # Уникальное имя пользователя
    password = db.Column(db.String(150), nullable=False)  # Хэшированный пароль

    # Связи: один пользователь — много целей и задач
    goals = db.relationship('Goal', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)

# Модель цели
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Название цели
    description = db.Column(db.Text, nullable=True)  # Описание цели (необязательно)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Владелец цели

    tasks = db.relationship('Task', backref='goal', lazy=True)  # Связанные задачи

# Модель задачи
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)  # Название задачи
    progress = db.Column(db.Integer, default=0)  # Прогресс выполнения (в процентах)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Владелец задачи
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))  # Связанная цель (необязательно)
