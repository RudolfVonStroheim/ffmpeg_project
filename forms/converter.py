from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired


class ConverterForm(FlaskForm):
    select_format = StringField("Формат", validators=[DataRequired()], default="Оставить")
    select_vcodec = StringField("Выберите кодек для видео", validators=[
                                DataRequired()], default="Оставить")
    select_acodec = StringField("Выберите кодек для звука", validators=[
                                DataRequired()], default="Оставить")
    select_scodec = StringField("Выберите кодек для субтитров", validators=[
                                DataRequired()], default="Оставить")
    video_streams = SelectMultipleField("Выберите видеодорожки", coerce=int)
    audio_streams = SelectMultipleField("Выберите аудиодорожки", coerce=int)
    sub_streams = SelectMultipleField("Выберите субтитры", coerce=int)
    submit = SubmitField("Конвертировать")
