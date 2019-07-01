import flask
from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_user

from app.models import User
from app.views import login_blue


@login_blue.route('/')
def index():
    return render_template('login.html')


@login_blue.route('/login/', methods=['GET', 'POST'])
def sign_in():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        # login_user(user, True)
        flask.flash('Logged in successfully.')
        # return redirect(url_for('home_blue.work_home'))

    return render_template('login.html')

#
# @login_blue.route('/add_user/<username>')
# def add_user(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         role = Role.query.filter_by(id=1).first()
#         if role is None:
#             role = Role(id=1, name='超级管理员', users='')
#         user = User(email='xwsftst@126.com', username=username, password='123456', role_id=role.id)
#     db.session.add(user)
#     db.session.commit()
#
#     return '添加用户'
#
#
# @login_blue.route('/add_role/<rid>')
# def add_role(rid):
#     print(rid)
#     role = Role.query.filter_by(id=int(rid)).first()
#     if role is None:
#         role = Role(id=int(rid), name='超级管理员')
#         db.session.add(role)
#         db.session.commit()
#     return '添加用户'
