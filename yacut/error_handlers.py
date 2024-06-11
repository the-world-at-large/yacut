from flask import render_template, jsonify

from . import app, db
from .constants import INTERNAL_SERVER_ERROR_TEMPLATE, PAGE_NOT_FOUND_TEMPLATE


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error):
    response = jsonify(error.to_dict())
    return response, error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template(PAGE_NOT_FOUND_TEMPLATE), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(INTERNAL_SERVER_ERROR_TEMPLATE), 500
