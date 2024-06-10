from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from . import app
from .services import create_short_url_service, get_original_url_service
from .error_handlers import InvalidAPIUsage


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

    try:
        url_map, short_id = create_short_url_service(original_link, custom_id)
    except ValueError as e:
        raise InvalidAPIUsage(str(e))

    short_link = request.host_url + short_id
    return jsonify({'short_link': short_link, 'url': url_map.original}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        original_url = get_original_url_service(short_id)
    except InvalidAPIUsage as e:
        raise e
    return jsonify({'url': original_url})
