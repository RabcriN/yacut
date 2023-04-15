from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


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
    if ('custom_id' not in data or data['custom_id'] is None or
            data['custom_id'] == ''):
        data['custom_id'] = URLMap.get_unique_short_id()
    URLMap.check_url(data['custom_id'])
    if URLMap.get_short_link(data['custom_id']):
        raise InvalidAPIUsage(
            f'''Имя "{data['custom_id']}" уже занято.''',
            400
        )
    link = URLMap()
    link.from_dict(data)
    URLMap.add_to_db(link)
    final_url = request.url_root + link.short
    return jsonify({'url': link.original, 'short_link': final_url}), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_link(short):
    link = URLMap.get_short_link(short)
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200