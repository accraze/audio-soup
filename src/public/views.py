# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_paginate import Pagination, get_page_args

from ..models import AudioFile


blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route('/', methods=["GET", "POST"])
def grid_view():
    audio_samples = AudioFile.query.all()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(audio_samples)
    pagination_samples = get_paginated_samples(
        audio_samples, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bulma')
    audio_grid = [pagination_samples[i * 3:(i + 1) * 3]
                  for i in range((len(pagination_samples) + 3 - 1) // 3)]

    return render_template('base.html', grid=audio_grid, page=page,
                           per_page=per_page,
                           pagination=pagination,)


def get_paginated_samples(samples, offset=0, per_page=9):
    return samples[offset: offset + per_page]


@blueprint.route('/sample/<file_name>')
def sample_review(file_name):
    print(file_name)
    return render_template('sample_review.html')


@blueprint.route('/feature_select/<ftype>')
def feature_select(ftype):
    return render_template('feature_select.html')
