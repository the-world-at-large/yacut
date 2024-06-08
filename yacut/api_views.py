import re
import random
import string

from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage


def get_unique_short_id():
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=6))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    try:
        data = request.get_json()
        if data is None:
            raise InvalidAPIUsage('Отсутствует тело запроса')
    except BadRequest:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    except Exception:
        raise InvalidAPIUsage('Ошибка обработки запроса')

    original_link = data.get('url')
    if not original_link:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя '
                                  'для короткой ссылки')
        elif not re.match(r'^[a-zA-Z0-9]*$', custom_id):
            raise InvalidAPIUsage('Указано недопустимое имя '
                                  'для короткой ссылки')
        elif URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки '
                                  'уже существует.')

    short_id = custom_id if custom_id else get_unique_short_id()

    url_map = URLMap(original=original_link, short=short_id)
    db.session.add(url_map)
    db.session.commit()

    short_link = request.host_url + short_id
    return jsonify({'short_link': short_link, 'url': original_link}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return jsonify({'url': url_map.original})
