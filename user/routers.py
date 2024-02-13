from flask import Blueprint, render_template, redirect, url_for, session
from app_database.connect import session_maker
from app_database.models import User
from .forms import CreateUserForm, LoginForm
from flask_login import login_user
from passlib.hash import pbkdf2_sha256
from app_utils.utils import set_username

user = Blueprint('user', __name__, template_folder='templates', static_folder='static')


@user.route('/create-user', methods=['GET', 'POST'])
def create_user():
    """Создание(добавления) пользователя"""
    form = CreateUserForm()
    response = {
        "create_form": True
    }
    if form.validate_on_submit():
        form_data = form.data
        password_hash = pbkdf2_sha256.hash(form_data['password'])
        try:
            with session_maker() as conn:
                new_user = User(
                    username=form_data['username'],
                    password=password_hash,
                    about_me=form_data['about_me']
                )
                conn.add(new_user)
                conn.commit()
                set_username(form)
                login_user(new_user)
                session.permanent = True
        except Exception as e:
            print(e)
            conn.rollback()
        return redirect(url_for('main_page'))

    print(form.errors.items())
    return render_template('create_or_login_user.html', response=response, form=form)


@user.route('/login-user', methods=['GET', 'POST'])
def user_login():
    """Авторизация пользователя"""
    form = LoginForm()
    response = {
        "login_form": True
    }
    if form.validate_on_submit():
        set_username(form)
        return redirect(url_for('main_page'))
    # TODO добавить код для показа ошибки
    return render_template('create_or_login_user.html', response=response, form=form)
