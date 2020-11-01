from flask import Flask, escape, request, render_template
import os

from .extensions import db
from .public import views

def register_extensions(app):
    db.init_app(app)

def create_app(config_object="src.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(views.blueprint)
    return None

app = create_app()


