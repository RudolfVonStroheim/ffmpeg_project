from flask import Flask, render_template, redirect
import os
from flask_wtf import FlaskForm
from sqlalchemy.sql.dml import ReturningDelete
from sqlalchemy.sql.operators import op
from werkzeug.utils import secure_filename
from data import db_session
from data.user import User
from data.conversion import Conversion
from converter import Converter
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user
from forms.file import UploadForm
from pickle import load

app = Flask(__name__)
login_m = LoginManager()
login_m.init_app(app)
app.config["MAX_CONTENT_LENGTH"] = 25 * 2 ** 22
app.config["UPLOAD_FOLDER"] = "input"
app.config["SECURITY_KEY"] = "kjhkshjhshdkhjsasjkhdkhskjhapchikhba"
f = open('formats.pickle', 'rb')
ALLOWED_EXTENSIONS = load(f)
f.close()


@login_m.user_loader
def get_user(user_id):
    sess = db_session.create_session()
    return sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('main.html', title='MPEG ONLINE: Easy video and audio converter tool.')

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(f'/convert/{filename}')
        else:
            return render_template('upload.html', title="Загрузка", msg="Недопустимый формат файла или превышен допустимый размер файла.", form=form)
    return render_template('upload.html', title="Загрузка", form=form)

@app.route('/convert')
def convert():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/profile")
        return render_template('login.html', title="Вход", message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Вход', form=form)


if __name__ == "__main__":
    db_session.global_init("db/converter.db")
    app.run("127.0.0.1", 8080)
