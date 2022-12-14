from flask import Flask, jsonify, request, redirect
from .config.config import Config
from .helpers import register_blueprints, register_extentions
from .extensions import db
from .config.logger import app_logger
from .helpers.hooks import (
    get_exception,
    get_response,
    log_get_request,
    log_post_request,
)
import os

def create_app(config_name='default'):
    """Create the flask app."""
    app = Flask(__name__)
    app.config.from_object(Config[config_name])
    
    @app.route('/')
    def index():
        return jsonify({'Hello': 'Form flask!'})
    
    
    register_extentions(app)
    register_blueprints(app)
    
    @app.before_first_request
    def application_startup():
        """Log the beginning of the application."""
        app_logger.info('Web app is up!')

    @app.before_request
    def log_request():
        """Log the data held in the request"""
        if request.method in ['POST', 'PUT']:
            log_post_request()
        elif request.method in ['GET', 'DELETE']:
            log_get_request()

    @app.after_request
    def log_response(response):
        try:
            get_response(response)
        except Exception:
            pass
        finally:
            return response

    @app.teardown_request
    def log_exception(exc):
        get_exception(exc)
        
    @app.route('/logs')
    def get_logs():
        host = os.environ['LOGGER_HOST']
        return redirect(f'{request.host_url.split(":")[0]}://{host}:5601')
    
    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": db})
    
    return app