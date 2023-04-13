from flask import jsonify, request

from . import app, db
from .models import URLMap
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            400
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!',
            400
        )
    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    if len(data['custom_id']) > 16:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки',
            400
        )
    not_valid = (".,/!?-@$АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                 "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
    for elem in data['custom_id']:
        if elem in not_valid:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400
            )
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            f'''Имя "{data['custom_id']}" уже занято.''',
            400
        )
    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    final_url = request.url_root + link.short
    return jsonify({'url': link.original, 'short_link': final_url}), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_link(short):
    link = URLMap.query.filter_by(short=short).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200