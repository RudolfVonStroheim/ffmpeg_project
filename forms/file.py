from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField("Выберите файл", validators=[FileRequired()])
    submit = SubmitField("Загрузить", validators=[DataRequired()])

