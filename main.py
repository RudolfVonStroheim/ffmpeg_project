from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from data import db_session
from data.user import User
from data.conversion import Conversion
from forms.user import RegisterForm, LoginForm, Error
from flask_login import LoginManager

app = Flask(__name__)
login_m = LoginManager()
login_m.init_app(app)

@login_m.user_loader
def get_user(user_id):
    sess = db_session.create_session()
    return sess.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('main.html', title='MPEG ONLINE: Easy video and audio converter tool.', log_st=0)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Регистрация", form=form, message="Пароли не совпадают")
        sess = db_session.create_session()
        if sess.query(User).filter(User.username == form.username.data).first():
            return render_template("register.html", title="Регистрация", form=form, message="Такой пользователь уже есть")
        user = User(name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title="Вход"
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Вход', form=form)
       
if __name__ == "__main__":
    db_session.global_init("db/converter.db")
    app.run("127.0.0.1", 8080)
