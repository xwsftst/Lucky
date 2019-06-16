import os
from datetime import datetime
from xml.etree import ElementTree

from flask import url_for
from flask_restful import reqparse, Resource
from sqlalchemy import and_

from app.ext import db
from app.models import User, Project, Task


class TaskApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('project_id', type=int, default=-1)
        self.parser.add_argument('task_id', type=int, default=-1)
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('rows', type=int, default=15)

    def get(self):
        args = self.parser.parse_args()
        if args["project_id"] == -1:
            pagination = Task.query.order_by(Task.id.desc()).paginate(
                args["page"], per_page=args["rows"],
                error_out=False
            )
        else:
            pagination = Task.query.filter_by(project_id=args["project_id"]).order_by(Task.id.desc()).paginate(
                args["page"], per_page=args["rows"],
                error_out=False
            )

        tasks = pagination.items
        data = {"total": pagination.total, "rows": []}
        urls = {
            "pass": "success.png",
            "fail": "fail.png",
            "running": "run.gif",
            "exception": "exception.png"
        }

        for task in tasks:
            if task.create_user_id is None:
                continue

            t = self.__check_task_status(task.project_id, task.build_no)
            data["rows"].append({
                "id": t.id,
                "status": t.status,
                "url": url_for('static', filename='img/%s' % urls[t.status]),
                "name": Project.query.filter_by(id=t.project_id).first().name,
                "build_no": t.build_no,
                "project_id": t.project_id,
                "cron": Project.query.filter_by(id=t.project_id).first().cron,
                "start_time": t.create_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": t.end_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "duration": "%s秒" % t.duration,
                "runner": User.query.filter_by(id=t.create_user_id).first().username
            })

        return data

    def __check_task_status(self, project_id, build_no):
        status = "running"
        output_dir = os.getcwd() + "/logs/%s/%s" % (project_id, build_no)
        task = Task.query.filter(and_(Task.project_id == project_id,
                                          Task.build_no == build_no)).first()
        if os.path.exists(output_dir + "/report.html"):
            tree = ElementTree.parse(output_dir + "/output.xml")
            root = tree.getroot()
            #passed = root.find("./statistics/suite/stat").attrib["pass"]
            fail = root.find("./statistics/suite/stat").attrib["fail"]

            if int(fail) != 0:
                status = 'fail'
                task.status = 'fail'
            else:
                status = 'pass'
                task.status = 'pass'
            starttime = datetime.strptime(root.find("./suite/status").attrib["starttime"], "%Y%m%d %H:%M:%S.%f")
            endtime = datetime.strptime(root.find("./suite/status").attrib["endtime"], "%Y%m%d %H:%M:%S.%f")
            task.create_timestamp = starttime
            task.end_timestamp = endtime
            task.duration = (endtime - starttime).seconds
            task.status = status
        else:
            now = datetime.now()
            seconds = (now - task.create_timestamp).seconds
            if seconds > 7200 and task.status != "exception":
                status = "exception"
                task.status = status
                task.end_timestamp = now
                task.duration = seconds

            task.end_timestamp = now

        db.session.merge(task)
        db.session.commit()

        return task