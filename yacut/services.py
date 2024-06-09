import re

from .models import URLMap
from .utils import generate_unique_short_id
from .error_handlers import InvalidAPIUsage


def create_short_url_service(data):
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    original_link = data.get('url')
    if not original_link:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > 16:
            raise InvalidAPIUsage('Указано недопустимое '
                                  'имя для короткой ссылки')
        elif not re.match(r'^[a-zA-Z0-9]*$', custom_id):
            raise InvalidAPIUsage('Указано недопустимое имя '
                                  'для короткой ссылки')
        elif URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage('Предложенный вариант короткой '
                                  'ссылки уже существует.')

    short_id = custom_id if custom_id else generate_unique_short_id()

    url_map = URLMap(original=original_link, short=short_id)
    return url_map, short_id


def get_original_url_service(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return url_map.original
