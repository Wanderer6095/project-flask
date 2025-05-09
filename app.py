# Основной файл приложения Flask

from flask import Flask, render_template
from flask_login import LoginManager, current_user
from models import db, User
from auth import auth_bp
from goals import goals_bp
from tasks import tasks_bp
from api import api_bp

app = Flask(__name__)

# Настройки конфигурации
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Настройка менеджера входа
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Функция для загрузки пользователя по ID (для Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Подключение всех маршрутов (blueprint'ов)
app.register_blueprint(auth_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(api_bp)

# Главная страница
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('profile.html')
    else:
        return render_template('login.html')

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание всех таблиц при первом запуске
    app.run(debug=True)