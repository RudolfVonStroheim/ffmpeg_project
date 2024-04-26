from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired


class ConverterForm(FlaskForm):
    select_format = SelectField("Формат", validators=[DataRequired()])
    select_vcodec = SelectField("Выберите кодек для видео", validators=[
                                DataRequired()], default="Оставить")
    select_acodec = SelectField("Выберите кодек для звука", validators=[
                                DataRequired()], default="Оставить")
    select_scodec = SelectField("Выберите кодек для субтитров", validators=[
                                DataRequired()], default="Оставить")
    video_streams = SelectMultipleField("Выберите видеодорожки", coerce=int)
    audio_streams = SelectMultipleField("Выберите аудиодорожки", coerce=int)
    sub_streams = SelectMultipleField("Выберите субтитры", coerce=int)
    submit = SubmitField("Конвертировать")
