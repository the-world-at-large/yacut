from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

from .constants import MAX_CUSTOM_ID_LENGTH, MAX_ORIGINAL_ID_LENGTH


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка', validators=[
            DataRequired(), URL(), Length(max=MAX_ORIGINAL_ID_LENGTH),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[
            Optional(), Length(max=MAX_CUSTOM_ID_LENGTH),
        ]
    )
    submit = SubmitField('Создать')
