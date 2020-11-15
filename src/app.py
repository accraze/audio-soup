from flask import Flask, escape, request, render_template
import os

from .extensions import db, migrate
from .filters import split_name, split_name_label
from .public import views

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

def create_app(config_object="src.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)
    register_filters(app)
    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(views.blueprint)
    return None

def register_filters(app):
    app.jinja_env.filters['split_name'] = split_name
    app.jinja_env.filters['split_name_label'] = split_name_label

app = create_app()
