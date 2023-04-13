from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, ValidationError


def validate_short(form, field):
    if field.data is not None:
        not_valid = (".,/!?-@$АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                     "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
        for elem in field.data:
            if elem in not_valid:
                raise ValidationError(
                    'Указано недопустимое имя для короткой ссылки'
                )


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
