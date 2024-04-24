from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from data import db_session
from data.user import User
from data.conversion import Conversion
from forms.user import RegisterForm, LoginForm, Error

app = Flask(__name__)

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
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login"):
    form = LoginForm()
    sess = db_session.create_session()
    if form.validate_on_submit():
        username = form.username.data
        passwd = form.password.data
        try:
            form.set_password(username)
        except Error as e:
            return render_template("login.html", title="Вход", form=form, message=e.msg)
        if form.check_password(passwd):
            return redirect("/profile")
        
if __name__ == "__main__":
    db_session.global_init("db/converter.db")
    app.run("127.0.0.1", 8080)
