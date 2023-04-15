from flask import flash, redirect, render_template, request

from . import app
from .forms import LinkForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if request.method == 'GET':
        return render_template('create_link.html', form=form), 200
    if not form.validate_on_submit():
        return render_template('create_link.html', form=form), 400
    custom_id = form.custom_id.data
    if custom_id == '' or custom_id is None:
        custom_id = URLMap.get_unique_short_id()
    if URLMap.get_short_link(custom_id):
        flash(f'Имя {custom_id} уже занято!')
        return render_template('create_link.html', form=form)
    url = URLMap(
        original=form.original_link.data,
        short=custom_id,
    )
    URLMap.add_to_db(url)
    final_url = request.base_url + custom_id
    return render_template(
        'create_link.html',
        form=form,
        final_url=final_url
    )


@app.route('/<string:short>')
def link_view(short):
    url = URLMap.get_short_link_or_404(short)
    return redirect(url.original)