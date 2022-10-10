from ..auth.views import auth
from ..flag.views import flag
from ..report.views import report
from ..suspend.views import suspend
from ..email.views import mail as mail_blueprint
from ..admin.views import admin
from ..author.views import author
from ..moderator.views import moderator
from flasgger import LazyJSONEncoder
from ..extensions import db, migrate, bcrypt, ma, cors, swagger, mail


def register_blueprints(app):
    """Register the application blueprints."""
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(report, url_prefix='/report')
    app.register_blueprint(flag, url_prefix='/flag')
    app.register_blueprint(suspend, url_prefix='/suspend')
    app.register_blueprint(mail_blueprint, url_prefix='/mail')
    app.register_blueprint(author, url_prefix='/author')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(moderator, url_prefix='/moderator')
    
def register_extentions(app):
    """Register the application extensions."""
    app.json_encoder = LazyJSONEncoder
    
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)
    mail.init_app(app)