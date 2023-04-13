import random
import string

from flask import flash, render_template, request, redirect

from . import app, db
from .forms import LinkForm
from .models import URLMap


def get_unique_short_id():
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for x in range(6)
    )


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if request.method == 'GET':
        return render_template('create_link.html', form=form), 200
    if request.method == 'POST':
        if form.validate_on_submit():
            custom_id = form.custom_id.data
            if custom_id == '' or custom_id is None:
                custom_id = get_unique_short_id()
            if URLMap.query.filter_by(short=custom_id).first():
                flash(f'Имя {custom_id} уже занято!')
                return render_template('create_link.html', form=form)
            url = URLMap(
                original=form.original_link.data,
                short=custom_id,
            )
            db.session.add(url)
            db.session.commit()
            final_url = request.base_url + custom_id
            return render_template(
                'create_link.html',
                form=form,
                final_url=final_url
            )
            return render_template('create_link.html', form=form), 200
        return render_template('create_link.html', form=form), 400


@app.route('/<string:short>')
def link_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)