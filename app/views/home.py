from flask import render_template
from flask_login import logout_user, login_required

from app.models import Permission
from . import home_blue


@home_blue.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@home_blue.route('/home/', methods=['POST', 'GET'])
def work_home():
    return render_template('home.html')


@home_blue.route('/logout/', methods=['POST', 'GET'])
@login_required
def sign_out():
    logout_user()
    return render_template('login.html')
