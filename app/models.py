from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.ext import db, login_manager


class Permission:
    """
    权限，这里暂时以角色代替
    """
    GUEST = 1
    PROJECT = 2
    MANAGER = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    def has_permission(self, perm):
        return self.permission & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permission += perm

    def reset_permission(self):
        self.permission = 0

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permission -= perm

    @staticmethod
    def insert_roles():
        roles = {
            "普通用户": [Permission.GUEST],
            "会员": [Permission.PROJECT, Permission.GUEST],
            "管理员": [Permission.MANAGER, Permission.PROJECT, Permission.GUEST],
            "超级管理员": [Permission.ADMIN, Permission.MANAGER, Permission.PROJECT, Permission.GUEST]
        }
        default_role = "普通用户"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    last_seen = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='超级管理员').first()
            if self.role is None:
                self.role = Role.query.filter_by(id=self.role_id).first()

    @staticmethod
    def insert_admin():
        email = current_app.config["FLASKY_ADMIN"]
        user = User.query.filter_by(email=email).first()
        if user is None:
            role = Role.query.filter_by(name='超级管理员').first()
            u = User(email=email, username="admin", password="123456", role_id=role.id)
            db.session.add(u)
            db.session.commit()

    @staticmethod
    def insert_manager():
        role = Role.query.filter_by(name='管理员').first()
        u = User(email="manager@126.com", username="lucky_manager", password="123456", role_id=role.id)
        db.session.add(u)
        db.session.commit()

    @staticmethod
    def insert_member():
        role = Role.query.filter_by(name='会员').first()
        u = User(email="member@126.com", username="lucky_member", password="123456", role_id=role.id)
        db.session.add(u)
        db.session.commit()

    @staticmethod
    def insert_user(email, username, password, role_name):
        user = User.query.filter_by(username=username).first()
        if user is None:
            role = Role.query.filter_by(name=role_name).first()
            user = User(email=email, username=username, password=password, role_id=role.id)
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError(u'文明密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Product(db.Model):
    """
    产品
    """
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    desc = db.Column(db.String(128), index=True)
    tags = db.Column(db.String(64), index=True)
    enable = db.Column(db.Boolean, default=True, index=True)

    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_timestamp = db.Column(db.DateTime, index=True, default=datetime.now())


class Project(db.Model):
    """
    项目
    """
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    product_id = db.Column(db.Integer)
    # product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    category = db.Column(db.String(64), index=True)
    desc = db.Column(db.String(128), index=True)
    tags = db.Column(db.String(64), index=True)
    enable = db.Column(db.Boolean, default=True, index=True)
    version = db.Column(db.String(32), index=True)
    cron = db.Column(db.Text)
    setup = db.Column(db.Text)
    teardown = db.Column(db.Text)

    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_timestamp = db.Column(db.DateTime, index=True, default=datetime.now())


class Task(db.Model):
    """
        任务
    """
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    #project_id = db.Column(db.Integer, db.ForeignKey('auto_project.id'))
    build_no = db.Column(db.Integer, index=True)
    status = db.Column(db.String(32), index=True)
    result = db.Column(db.String(32), index=True)
    duration = db.Column(db.Integer)
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    end_timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
