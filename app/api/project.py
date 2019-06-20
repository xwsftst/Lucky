from datetime import datetime

from flask import current_app
from flask_login import current_user
from flask_restful import Resource, reqparse

from app.ext import db
from app.models import Project, Product, User, UserKeywordSuite, UserKeyword, Var, Object, Case, Suite, Step


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
        self.parser.add_argument('enable', type=bool, default=False)
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

    def __get_suites_by_project_id(self, id):
        children = []
        suites = Suite.query.filter_by(project_id=id).order_by(Suite.id.asc()).all()
        for suite in suites:
            cases = self.__get_cases_by_suite_id(suite.id)
            children.append({
                "id": suite.id,
                "text": suite.name,
                "iconCls": "icon-suite",
                "attributes": {
                    "category": "suite",
                    "id": suite.id,
                    "project_id": suite.project_id,
                    "name": suite.name,
                    "desc": suite.desc
                },
                "children": cases

            })

        return children

    def __get_cases_by_suite_id(self, id):
        children = []
        cases = Case.query.filter_by(suite_id=id).order_by(Case.id.asc()).all()
        for case in cases:
            steps = self.__get_steps_by_case_id(case.id)
            children.append({
                "id": case.id,
                "text": case.name,
                "iconCls": "icon-case",
                "attributes": {
                    "category": "case",
                    "id": case.id,
                    "suite_id": case.suite_id,
                    "name": case.name,
                    "desc": case.desc
                },
                "children": steps
            })

        return children

    def __get_steps_by_case_id(self, id):
        children = []
        steps = Step.query.filter_by(case_id=id).order_by(Step.id.asc()).all()
        for step in steps:
            children.append({
                "id": step.id,
                "text": step.keyword,  # .split(".")[1],
                "iconCls": "icon-step",
                "attributes": {
                    "keyword": step.keyword,
                    "category": "step",
                    "id": step.id,
                    "case_id": step.case_id,
                    "desc": step.desc,
                    "param_1": step.param_1,
                    "param_2": step.param_2,
                    "param_3": step.param_3,
                    "param_4": step.param_4
                }})

        return children

    def __get_object_suites_by_project_id(self, id):
        children = []
        objects = Object.query.filter_by(project_id=id).order_by(Object.id.asc()).all()

        for obj in objects:
            vars = self.__get_var_by_object_id(obj.id)
            children.append({
                "id": obj.id,
                "text": obj.name,
                "iconCls": "icon-object",
                "attributes": {
                    "category": obj.category,
                    "id": obj.id,
                    "project_id": obj.project_id,
                    "name": obj.name,
                    "desc": obj.desc
                },
                "children": vars

            })

        return children

    def __get_keyword_suites_by_project_id(self, id):
        children = []
        suites = UserKeywordSuite.query.filter_by(project_id=id).order_by(UserKeywordSuite.id.asc()).all()

        for suite in suites:
            keys = self.__get_keyword_by_suite_id(suite.id)
            children.append({
                "id": suite.id,
                "text": suite.name,
                "iconCls": "icon-user_keyword",
                "attributes": {
                    "category": suite.category,
                    "id": suite.id,
                    "project_id": suite.project_id,
                    "name": suite.name,
                    "desc": suite.desc
                },
                "children": keys

            })

        return children

    def __get_keyword_by_suite_id(self, id):
        children = []
        keys = UserKeyword.query.filter_by(keyword_suite_id=id).order_by(UserKeyword.id.asc()).all()
        for k in keys:
            children.append({
                "id": k.id,
                "text": k.keyword,
                "iconCls": "icon-keyword",
                "attributes": {
                    "category": "user-keyword",
                    "id": k.id,
                    "suite_id": k.keyword_suite_id,
                    "keyword": k.keyword,
                    "params": k.params
                }})

        return children

    def __get_var_by_object_id(self, id):
        children = []
        vars = Var.query.filter_by(object_id=id).order_by(Var.id.asc()).all()
        for var in vars:
            children.append({
                "id": var.id,
                "text": var.name,
                "iconCls": "icon-var",
                "attributes": {
                    "category": var.category,
                    "id": var.id,
                    "object_id": var.object_id,
                    "name": var.name,
                    "value": var.value,
                    "desc": var.desc
                }})

        return children
