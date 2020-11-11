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

import librosa.display
import librosa
import matplotlib.pylab as plt
import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


from ..models import AudioFile, Label
from ..extensions import db


blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route('/', methods=["GET", "POST"])
def grid_view():
    if request.method == "POST":
        print(request.form)
        sample = AudioFile.query.get(request.form.get('_id'))
        sample.label_id = request.form.get('label'),
        sample.sample_rate = request.form.get('sample_rate'),
        sample.text = request.form.get('text')
        db.session.commit()
        flash('Audio sample metadata was successfully updated.')
        return redirect(url_for('public.grid_view'))
    label_filter = request.args.get('label_filter', None)
    if not label_filter:
        audio_samples = AudioFile.query.all()
    else:
        audio_samples = AudioFile.query.filter(AudioFile.label_id != label_filter).all()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(audio_samples)
    pagination_samples = get_paginated_samples(
        audio_samples, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bulma')
    audio_grid = [pagination_samples[i * 3:(i + 1) * 3]
                  for i in range((len(pagination_samples) + 3 - 1) // 3)]

    labels = Label.query.all()

    return render_template('sample_review.html', grid=audio_grid, page=page,
                           per_page=per_page,
                           pagination=pagination, labels=labels)


def get_paginated_samples(samples, offset=0, per_page=9):
    return samples[offset: offset + per_page]


@blueprint.route('/sample/<file_name>')
def sample_review(file_name):
    print(file_name)
    return render_template('sample_review.html')


@blueprint.route('/feature_select/<sample_id>')
def feature_select(sample_id, feature_type='spectral'):
    sample = AudioFile.query.get(sample_id)
    return render_template('feature_select.html', sample=sample, feature_type=feature_type)


@blueprint.context_processor
def utility_processor():
  def waveform_image(audiofile):
    try:
      y, sr = librosa.load('static/dataset/'+audiofile)
    except:
      y = []
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.grid()
    axis.plot(y)
    plt.axis('off')
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String
  return dict(waveform_image=waveform_image)
