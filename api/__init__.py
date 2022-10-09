from flask import Flask, jsonify
from .extensions import db, migrate, bcrypt, ma, cors, swagger
from .config import Config
from flasgger import LazyJSONEncoder
from .auth.views import auth


def create_app(config_name='default'):
    """Create the flask app."""
    app = Flask(__name__)
    app.config.from_object(Config[config_name])
    
    @app.route('/')
    def index():
        return jsonify({'Hello': 'Form flask!'})
    
    app.json_encoder = LazyJSONEncoder
    
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)
    
    app.register_blueprint(auth, url_prefix='/auth')
    
    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": db})
    
    return app