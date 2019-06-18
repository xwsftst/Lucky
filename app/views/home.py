import codecs
import os
import platform

from flask import render_template, send_file
from flask_login import logout_user, login_required

from app.decoradors import admin_required
from app.models import Permission
from app.utils.report import Report
from app.utils.runner import run_process
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


@home_blue.route('/test_run/<category>/<id>', methods=['GET'])
@login_required
def test_run(category, id):
    status = run_process(category, id)

    return status


@home_blue.route('/task/<id>', methods=['GET'])
@login_required
def task(id):
    return render_template('task.html', id=id)


@home_blue.route('/task_list', methods=['GET'])
@login_required
def task_list():
    return render_template('task_list.html')


@home_blue.route('/report/<project_id>/<build_no>', methods=['GET'])
@login_required
def report(project_id, build_no):
    r = Report(project_id, build_no)

    return r.build_report()


@home_blue.route('/run_logs/<project_id>/<build_no>', methods=['GET'])
@login_required
def run_logs(project_id, build_no):
    log_path = os.getcwd() + "/logs/%s/%s/logs.log" % (project_id, build_no)
    log_path = log_path.replace("\\", "/")
    logs = "还没捕获到日志信息^_^"
    if os.path.exists(log_path):
        if "Windows" in platform.platform():
            f = codecs.open(log_path, "r", "cp936")
        else:
            f = codecs.open(log_path, "r", "utf-8")

        logs = f.read()
        f.close()
        """
        app = current_app._get_current_object()
        for r in app.config["RUNNERS"]:
            p = r["runner"]
            if p._process.returncode == 0:
                print('Subprogram success')
                app.config["RUNNERS"].remove(r)
        """

    return render_template('logs.html', logs=logs)


@home_blue.route('/view_image/<project_id>/<build_no>/<filename>', methods=['GET'])
@login_required
def view_image(project_id, build_no, filename):

    img_path = os.getcwd() + "/logs/%s/%s/images/%s" % (project_id, build_no, filename)
    img_path.replace("\\", "/")
    if os.path.exists(img_path):
        return send_file(img_path)

    return "截图失败，木有图片!!!"


@home_blue.route('/detail/<project_id>/<build_no>', methods=['POST'])
@login_required
def detail(project_id, build_no):
    r = Report(project_id, build_no)
    import json
    return json.dumps(r.parser_detail_info())
