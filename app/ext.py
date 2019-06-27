from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

login_manager = LoginManager()
mail = Mail()


def init_ext(app):
    db.init_app(app=app)
    migrate = Migrate(app, db)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)
    login_manager.login_view = 'login.sign_in'
    mail.init_app(app)
