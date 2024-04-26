from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField("Выберите файл(до 100Мб)", validators=[DataRequired()])
    submit = SubmitField("Загрузить", validators=[DataRequired()])

