from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import EqualTo, DataRequired, ValidationError
from app_database.url_database import secret_register_key
from app_database.connect import session_maker
from sqlalchemy import select
from app_database.models import User
from passlib.hash import pbkdf2_sha256
from flask_login import login_user
from flask import session


def validate_secret_key(field):
    """Проверка секретного ключа"""
    if field.data != secret_register_key:
        raise ValidationError('The secret key does not match')


class CreateUserForm(FlaskForm):
    """Создание ползователя"""
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password confirm',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    about_me = TextAreaField('About', validators=[DataRequired()])
    secret_key = StringField('Secret Register Key', validators=[DataRequired()])
    submit = SubmitField('Create user')

    def validate_secret_key(self, field):
        validate_secret_key(field)


class LoginForm(FlaskForm):
    """Вход пользователя"""
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    secret_key = StringField('Secret Register Key', validators=[DataRequired()])
    submit = SubmitField('Login user')

    def validate_username(self, field):
        password = self.password.data
        try:
            with session_maker() as conn:
                query = select(User).filter_by(username=field.data)
                user = conn.execute(query).scalars().first()
                if not user:
                    raise ValidationError('Invalid username')
                if not pbkdf2_sha256.verify(password, user.password):
                    raise ValidationError('Invalid password')
        except Exception as e:
            raise ValidationError(e)
        login_user(user)
        session.permanent = True

    def validate_secret_key(self, field):
        validate_secret_key(field)
