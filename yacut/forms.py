from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length

from .models import URLMap


def validate_short(form, field):
    if field.data is not None:
        URLMap.check_url(field.data)


class LinkForm(FlaskForm):

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(0, 16, message=(
            'Ссылка должна содержать максимум %(max)d знаков')),
            validate_short]
    )
    submit = SubmitField('Жмяк')
