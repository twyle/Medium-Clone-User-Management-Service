from flask import Flask, jsonify
from .config import Config
from .helpers import register_blueprints, register_extentions
from .extensions import db


def create_app(config_name='default'):
    """Create the flask app."""
    app = Flask(__name__)
    app.config.from_object(Config[config_name])
    
    @app.route('/')
    def index():
        return jsonify({'Hello': 'Form flask!'})
    
    
    register_extentions(app)
    register_blueprints(app)
    
    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": db})
    
    return app