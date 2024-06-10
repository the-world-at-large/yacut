import re

from .models import URLMap
from .utils import generate_unique_short_id
from .constants import MAX_CUSTOM_ID_LENGTH, CUSTOM_ID_REGEX
from .error_handlers import InvalidAPIUsage
from . import db


def create_short_url_service(original_link, custom_id=None):
    if custom_id:
        if len(custom_id) > MAX_CUSTOM_ID_LENGTH:
            raise ValueError('Указано недопустимое имя для короткой ссылки')
        if not re.match(CUSTOM_ID_REGEX, custom_id):
            raise ValueError('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first():
            raise ValueError('Предложенный вариант короткой ссылки '
                             'уже существует.')

    short_id = custom_id if custom_id else generate_unique_short_id()
    url_map = URLMap(original=original_link, short=short_id)

    try:
        db.session.add(url_map)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return url_map, short_id


def get_original_url_service(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return url_map.original
