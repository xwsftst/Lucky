from flask import url_for
from flask_login import login_user, logout_user
from flask_restful import Resource, reqparse

from app.models import User


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('method', type=str)

    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args["password"]
        method = args["method"]
        if method == 'sign_in':
            user = User.query.filter_by(username=username).first()
            if user is not None and user.verify_password(password):
                login_user(user, True)
                return {
                    'status': 'success',
                    'msg': '欢迎登录Lucky自动化测试平台！',
                    'url': url_for('home.work_home')
                }, 201
            return {
                'status': 'fail',
                'msg': '用户名或密码错误！',
                'url': url_for('login.index')
            }, 201
        elif method == 'logout':
            logout_user()
            return {
                'status': 'success',
                'msg': '退出成功！',
                'url': url_for('home.logout')
            }, 201
        return {
                'status': 'success',
                'msg': '返回登录页面',
                'url': url_for('login.sign_in')
         }, 201
