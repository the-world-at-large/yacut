import random
import string

from .models import URLMap
from .constants import CUSTOM_ID_LENGTH


def generate_unique_short_id():
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=CUSTOM_ID_LENGTH))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
