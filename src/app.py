from flask import Flask, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return render_template('base.html')

@app.route('/sample/<file_name>')
def sample_review(file_name):
    print(file_name)
    return render_template('sample_review.html')

@app.route('/feature/<f_type>')
def plot_feature(f_type):
    pass
