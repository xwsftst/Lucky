from flask import Blueprint
from flask_restful import Api

api_blue = Blueprint('api', __name__)
api = Api(api_blue)


def init_api(app):
    app.register_blueprint(blueprint=api_blue, url_prefix='/api/v1')


from .login import Login
api.add_resource(Login, '/login/')
