from flask import Blueprint


login_blue = Blueprint('login', __name__)
home_blue = Blueprint('home', __name__)


def init_views(app):
    app.register_blueprint(blueprint=login_blue)
    app.register_blueprint(blueprint=home_blue)


from . import login
from . import home
