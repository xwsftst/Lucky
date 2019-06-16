from flask import current_app
from flask_restful import Resource, reqparse

from app.ext import db
from app.models import Project


class TriggerApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('trigger_id', type=int, default=-1)
        self.parser.add_argument('method', type=str, default="start")
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('rows', type=int, default=15)

    def get(self):

        app = current_app._get_current_object()

        return app.config["TRIGGER"].get_jobs()

    def post(self):
        result = {"status": "success",
                  "msg": "操作成功"}
        args = self.parser.parse_args()

        app = current_app._get_current_object()
        enable = True

        try:
            if args["method"] == "start":
                enable = True
                app.config["TRIGGER"].update_job(args["trigger_id"])
            elif args["method"] == "stop":
                enable = False
                app.config["TRIGGER"].remove_job(args["trigger_id"])

            p = Project.query.filter_by(id=args["trigger_id"]).first()
            p.enable = enable
            db.session.merge(p)
            db.session.commit()
        except Exception as e:
            result["status"] = "fail"
            result["msg"] = "调度失败: %s" % str(e)

        app.config["TRIGGER"].load_job_list()
        return result, 201