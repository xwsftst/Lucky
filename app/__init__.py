from flask import Flask

from app.api import init_api
from app.ext import init_ext
from app.settings import environments
from app.views import init_views


def create_app():
    app = Flask(__name__)
    app.config.from_object(environments.get('develop'))
    init_ext(app)
    init_views(app)
    init_api(app)

    return app
