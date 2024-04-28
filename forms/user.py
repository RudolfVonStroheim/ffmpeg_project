from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, EmailField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired


class Error(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class RegisterForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Введите пароль", validators=[DataRequired()])
    password_again = PasswordField(
        "Повторите пароль", validators=[DataRequired()])
    username = StringField("Имя пользователя", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField('Войти')

    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)



