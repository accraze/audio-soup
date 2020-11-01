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

from ..models import AudioFile


blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route('/', methods=["GET", "POST"])
def grid_view():
    name = request.args.get("name", "World")
    audio_samples = AudioFile.query.all()
    audio_grid = [audio_samples[i * 3:(i + 1) * 3]
                  for i in range((len(audio_samples) + 3 - 1) // 3)]
    return render_template('base.html', grid=audio_grid)


@blueprint.route('/sample/<file_name>')
def sample_review(file_name):
    print(file_name)
    return render_template('sample_review.html')


@blueprint.route('/feature_select/<ftype>')
def feature_select(ftype):
    return render_template('feature_select.html')
