from flask import render_template, flash, redirect, request

from . import app, db
from .forms import URLForm
from .models import URLMap
import random
import string


def get_unique_short_id():
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=6))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    short_id = None
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                flash('Предложенный вариант короткой ссылки уже существует.',
                      'error')
                return render_template('index.html', form=form)
            short_id = custom_id
        else:
            short_id = get_unique_short_id()

        url_map = URLMap(original=original_link, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return render_template(
            'index.html', form=form, short_link=request.host_url + short_id)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
