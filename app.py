import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager

from app_database.connect import session_maker
from app_database.models import User, Experience
from user.routers import user
from user_expirience.routers import expirience
from user_skills.routers import skills
from app_file_resume.routers import router_file
from tasks.tasks import send_email, send_telegram_chat
from sqlalchemy import select
from sqlalchemy.orm import joinedload, contains_eager
from app_utils.utils import messages_errors_conn_db

load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/images/icon/skills-icon'

app.register_blueprint(user)
app.register_blueprint(expirience)
app.register_blueprint(skills)
app.register_blueprint(router_file)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.user_login'


@app.route('/')
def main_page():
    """
    Рендерит главную страницу
    """
    with session_maker() as conn:
        try:
            query = (
                select(User)
                .join(User.experiences)
                .options(contains_eager(User.experiences))
                .options(joinedload(User.skills))
                .filter(Experience.published)
            )
            content = conn.execute(query).scalars().first()
            return render_template('index.html', content=content)
        except Exception as err:
            messages_errors_conn_db(err, conn, 'error')
    return render_template('index.html')


@app.route('/send-message', methods=['POST'])
def send_message():
    """
    Отправка сообщени на email и telegram
    """
    form_data = request.form
    name = form_data['name']
    email = form_data['email']
    message = form_data['message']
    message_email = f'Name: {name}\nEmail: {email}\nMessage: {message}'
    result = send_email.delay(
        emails_list=os.getenv('SMTP_USER'),
        from_email=os.getenv('SMTP_USER'),
        subject=f'Message from user: {name.title()}',
        message=message_email
    )
    send_telegram_chat.delay(messages=message_email)  # отправляем ссобщение в телеграмм
    result.wait()  # Ждем, пока задача завершится
    response = {
        'status': result.result,
    }
    return jsonify(response)


@login_manager.user_loader
def load_user(user_id):
    with session_maker() as conn:
        return conn.get(User, int(user_id))

# if __name__ == '__main__':
#     app.run()
