from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# @manager.command
# def deploy():
#     from flask_migrate import upgrade
#     from app.models import Role, User
#     """
#     初始化角色和用户数据
#     """
#     upgrade()
#     Role.insert_roles()
#     User.insert_admin()
#     User.insert_manager()
#     User.insert_member()
#     User.insert_user("user2@126.com", "lucky_user2", "123456", "普通用户")


if __name__ == '__main__':
    manager.run()
