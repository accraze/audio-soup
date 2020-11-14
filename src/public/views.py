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
import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


from ..models import AudioFile, Label
from ..extensions import db


blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route('/', methods=["GET", "POST"])
def grid_view():
    if request.method == "POST":
        sample = AudioFile.query.get(request.form.get('_id'))
        sample.label_id = request.form.get('label'),
        sample.sample_rate = request.form.get('sample_rate'),
        sample.text = request.form.get('text')
        db.session.commit()
        flash('Audio sample metadata was successfully updated.')
        return redirect(url_for('public.grid_view'))
    label_filter = request.args.get('label_filter', None)
    if not label_filter:
        audio_samples = AudioFile.query.order_by('id').all()
    else:
        audio_samples = AudioFile.query.filter(AudioFile.label_id != label_filter).order_by('id').all()
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


def extract_melspectrogram(sample):
    try:
      y, sr = librosa.load('static/dataset/'+sample.name)
    except:
      y = []
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    fig = Figure()
    #axis = fig.add_subplot(1, 1, 1)
    #axis.grid()
    #canvas = FigureCanvas(fig)
    ax = fig.add_subplot(1,1,1)
    p = librosa.display.specshow(librosa.power_to_db(S),ax=ax, y_axis='log', x_axis='time')
    #axis.plot(librosa.power_to_db(S))
    fig.colorbar(p, format='%+2.0f dB')
    #plt.axis('off')
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


def extract_tonnetz_chroma(sample):
    try:
      y, sr = librosa.load('static/dataset/'+sample.name)
    except:
      y = []
    y = librosa.effects.harmonic(y)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    fig = Figure()
    ax = fig.add_subplot(2,1,1)
    p = librosa.display.specshow(tonnetz,ax=ax, y_axis='tonnetz')
    fig.colorbar(p)
    ax2 = fig.add_subplot(2,1,2)
    q = librosa.display.specshow(librosa.feature.chroma_cqt(y, sr=sr), ax=ax2,
                         y_axis='chroma', x_axis='time')
    fig.colorbar(q)
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

def extract_power_contrast(sample):
    try:
      y, sr = librosa.load('static/dataset/'+sample.name)
    except:
      y = []
    S = np.abs(librosa.stft(y))
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    fig = Figure()
    ax = fig.add_subplot(2,1,1)
    ax.set(title='Power Spectrogram')
    p = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),ax=ax, y_axis='log')
    fig.colorbar(p, format='%+2.0f dB')
    ax.label_outer()
    ax2 = fig.add_subplot(2,1,2)
    ax2.set(title='Spectral Contrast', ylabel='Frequency bands')
    q = librosa.display.specshow(contrast, ax=ax2, x_axis='time')
    fig.colorbar(q)
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


@blueprint.route('/sample/<file_name>')
def sample_review(file_name):
    print(file_name)
    return render_template('sample_review.html')


@blueprint.route('/feature_select/<sample_id>')
def feature_select(sample_id, feature_type='spectral'):
    sample = AudioFile.query.get(sample_id)
    features = {}
    if feature_type == 'spectral':
        features['melspec'] =  extract_melspectrogram(sample)
        features['tonnetz'] = extract_tonnetz_chroma(sample)
        features['power'] = extract_power_contrast(sample)
    return render_template('feature_select.html', sample=sample, feature_type=feature_type, features=features)


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
    #plt.axis('off')
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String
  return dict(waveform_image=waveform_image)
