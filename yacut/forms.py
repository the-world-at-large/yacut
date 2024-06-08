from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка', validators=[DataRequired(), URL(), Length(max=512)])
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[Optional(), Length(max=16)])
    submit = SubmitField('Создать')
