from flask import render_template
from flask_login import logout_user, login_required

from app.decoradors import admin_required
from app.models import Permission
from . import home_blue


@home_blue.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@home_blue.route('/home/', methods=['GET'])
@login_required
def work_home():
    return render_template('home.html')


@home_blue.route('/logout/', methods=['GET'])
@login_required
def sign_out():
    logout_user()
    return render_template('login.html')


@home_blue.route('/product/', methods=['GET'])
@login_required
def product():
    return render_template('product.html')


@home_blue.route('/project/', methods=['GET'])
@login_required
def project():
    return render_template('project.html')


@home_blue.route('/user/', methods=['GET'])
@login_required
@admin_required
def user():
    return render_template('user.html')


@home_blue.route('/manage/<category>/<id>', methods=['GET'])
@login_required
def manage(category, id):
    return render_template('%s.html' % category, id=id)


@home_blue.route('/help/', methods=['GET'])
@login_required
def help():
    return render_template('help.html')
