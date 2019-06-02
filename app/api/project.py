from datetime import datetime

from flask import current_app
from flask_login import current_user
from flask_restful import Resource, reqparse

from app.ext import db
from app.models import Project, Product, User


class ProjectApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, default=-1)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('product_id', type=int)
        self.parser.add_argument('category', type=str)
        self.parser.add_argument('desc', type=str)
        self.parser.add_argument('version', type=str)
        self.parser.add_argument('tags', type=str)
        self.parser.add_argument('enable', type=bool, default=True)
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('cron', type=str)
        self.parser.add_argument('setup', type=str)
        self.parser.add_argument('teardown', type=str)

        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('rows', type=int, default=15)

    def get(self):
        args = self.parser.parse_args()
        if args["id"] == -1:

            pagination = Project.query.order_by(Project.id.desc()).paginate(
                args["page"], per_page=args["rows"],
                error_out=False
            )
            projects = pagination.items
            data = {"total": pagination.total, "rows": []}

            status = {True: "激活", False: "不可用"}
            for p in projects:
                data["rows"].append({
                    "id": p.id,
                    "name": p.name,
                    "product_id": p.product_id,
                    "product_name": Product.query.filter_by(id=p.product_id).first().name,
                    "category": p.category,
                    "desc": p.desc,
                    "cron": p.cron,
                    "enable": status[p.enable],
                    "create_user": User.query.filter_by(id=p.create_user_id).first().username,
                    "create_timestamp": p.create_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "update_user": User.query.filter_by(id=p.update_user_id).first().username,
                    "update_timestamp": p.update_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                })
        else:
            project = Project.query.filter_by(id=args["id"]).first()
            children = []
            if project:
                # 对象集
                children.extend(self.__get_object_suites_by_project_id(project.id))

                # 自定义关键字
                children.extend(self.__get_keyword_suites_by_project_id(project.id))

                # 套件集
                children.extend(self.__get_suites_by_project_id(project.id))

            return [{
                "id": project.id,
                "text": project.name,
                "iconCls": "icon-project",
                "attributes": {
                    "category": "project",
                    "id": project.id,
                    "name": project.name,
                    "desc": project.desc,
                    "cron": project.cron
                },
                "children": children
            }]

        return data

    def post(self):
        args = self.parser.parse_args()
        import json

        method = args["method"].lower()
        if method == "create":
            return self.__create(args), 201
        elif method == "edit":
            return self.__edit(args), 201
        elif method == "delete":
            return self.__delete(args), 201
        elif method == "query":
            return self.__query(args), 201

        return {"status": "fail", "msg": "方法: %s 不支持" % method}, 201

    def __create(self, args):
        result = {"status": "success",
                  "msg": "操作成功"}

        project = Product.query.filter_by(name=args["name"]).first()
        if project is None:
            try:
                project = Project(name=args["name"],
                                  desc=args["desc"],
                                  category=args["category"],
                                  product_id=args["product_id"],
                                  tags=args["tags"],
                                  enable=args["enable"],
                                  version=args["version"],
                                  cron=args["cron"],
                                  setup=args["setup"],
                                  teardown=args["teardown"],
                                  create_user_id=current_user.get_id(),
                                  update_user_id=current_user.get_id())

                db.session.add(project)
                db.session.commit()
                # app = current_app._get_current_object()
                # app.config["TRIGGER"].load_job_list()
            except Exception as e:
                result["status"] = "fail"
                result["msg"] = "异常：%s" % str(e)
        else:
            result["status"] = "fail"
            result["msg"] = "项目名称[%s]重复" % args["name"]

        return result

    def __edit(self, args):
        result = {"status": "success",
                  "msg": "操作成功"}
        project = Project.query.filter_by(id=args["id"]).first()
        if project is None:
            result["status"] = "fail"
            result["msg"] = "未找到要修改的项目id"
        else:
            try:
                project.category = args["category"]
                project.product_id = args["product_id"]
                project.name = args["name"]
                project.desc = args["desc"]
                project.tags = args["tags"]
                project.enable = args["enable"]
                project.version = args["version"]
                project.cron = args["cron"]
                project.setup = args["setup"]
                project.teardown = args["teardown"]

                project.update_user_id = current_user.get_id()
                project.update_timestamp = datetime.now()

                db.session.merge(project)
                db.session.commit()

                app = current_app._get_current_object()

                app.config["TRIGGER"].update_job(args["id"])

            except Exception as e:
                result["status"] = "fail"
                result["msg"] = "编辑项目[id-%s]失败：%s" % (args["id"], str(e))

        return result

    def __query(self, args):
        data = {"rows": []}
        if args["id"] == -1:
            status = {True: "激活", False: "不可用"}
            projects = Project.query.all()
            for p in projects:
                data["rows"].append({
                    "id": p.id,
                    "name": p.name,
                    "category": p.category,
                    "product_name": Product.query.filter_by(id=p.product_id).first().name,
                    "desc": p.desc,
                    "enable": status[p.enable],
                    "create_user": User.query.filter_by(id=p.create_user_id).first().username,
                    "create_timestamp": p.create_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "update_user": User.query.filter_by(id=p.update_user_id).first().username,
                    "update_timestamp": p.update_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                })
        elif args["id"] == -2:
            # 简略信息
            projects = Project.query.all()
            for p in projects:
                data["rows"].append({
                    "id": p.id,
                    "name": p.name
                })

        return data

    def __delete(self, args):
        result = {"status": "success",
                  "msg": "操作成功"}

        project = Project.query.filter_by(id=args["id"]).first()
        if project is None:
            result["status"] = "fail"
            result["msg"] = "未找到要删除的项目id"
        else:
            try:
                app = current_app._get_current_object()
                app.config["TRIGGER"].remove_job(args["id"])

                db.session.delete(project)
                db.session.commit()
            except Exception as e:
                result["status"] = "fail"
                result["msg"] = "删除项目[id-%s]失败：%s" % (args["id"], str(e))

        return result
