from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, SubmitField
from werkzeug import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
from ..data import db_session
from ..data.user import User


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

    def set_password(username):
        sess = db_session.create_session()
        if not sess.query(User).filter(User.username == username).first:
            raise Error("Такого пользователя нет")
        self.hashed_password = sess.query(User).filter(User.username == username).first()

    def check_password(self, passwd):
        return check_password_hash(self.hashed_password, passwd)
