from flask import render_template, flash, redirect, request

from . import app
from .error_handlers import InvalidAPIUsage
from .forms import URLForm
from .services import create_short_url_service, get_original_url_service


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    short_id = None
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        try:
            url_map, short_id = create_short_url_service(original_link,
                                                         custom_id)
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('index.html', form=form)

        return render_template(
            'index.html', form=form, short_link=request.host_url + short_id)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_url(short_id):
    try:
        original_url = get_original_url_service(short_id)
    except InvalidAPIUsage:
        return render_template('404.html'), 404
    return redirect(original_url)
