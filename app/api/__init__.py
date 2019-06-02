from flask import Blueprint
from flask_restful import Api

api_blue = Blueprint('api', __name__)
api = Api(api_blue)


def init_api(app):
    app.register_blueprint(blueprint=api_blue, url_prefix='/api/v1')


from .login import Login
from .product import ProductApi
from .project import ProjectApi
from .user import UserApi
from .role import RoleApi

api.add_resource(Login, '/login/')
api.add_resource(ProductApi, '/product/')
api.add_resource(ProjectApi, '/project/')
api.add_resource(UserApi, '/user/')
api.add_resource(RoleApi, '/role/')
