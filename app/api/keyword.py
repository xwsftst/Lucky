from flask_restful import Resource, reqparse
from app.models import Project, Object, Var, UserKeywordSuite, UserKeyword
from app.utils.parsing import parser_html


class KeywordApi(Resource):
    def __init__(self):
        print('KeywordApi)_)_)_)_)_)_)_)_)_)_)_)_)_)_)_)_')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('project_id', type=int, default=-1)

    def get(self):
        args = self.parser.parse_args()
        if args["project_id"] != -1:
            children = []
            project = Project.query.filter_by(id=args["project_id"]).first()
            if project:
                children.extend(self.get_objects(project.id))

            keyword_list = [{
                "id": project.id,
                "text": project.name,
                "state": "closed",
                "iconCls": "icon-project",
                "children": children
            }]
            return keyword_list

        # return parser()
        return parser_html()

    def post(self):
        args = self.parser.parse_args()

        # keyword_list = []
        if args["project_id"] != -1:
            children = []
            project = Project.query.filter_by(id=args["project_id"]).first()
            if project:
                children.extend(self.get_objects(project.id))

            keyword_list = [{
                "id": project.name,
                "text": project.name,
                "state": "closed",
                "iconCls": "icon-project",
                "children": children
            }]

            keyword_list.extend(self.get_keyword_suites(project.id))

            keyword_list.extend(parser_html(project.category))
            # keyword_list.extend(parser(project.category))
            return keyword_list

        return [{"id": 1, "text": "糟糕没有关键字..."}]

    def get_objects(self, project_id):
        children = []
        objects = Object.query.filter_by(project_id=project_id).order_by(Object.id.asc()).all()

        for obj in objects:
            variables = self.get_vars(obj.id)
            if len(variables) == 0:
                state = "open"
            else:
                state = "closed"
            children.append({
                "id": obj.name,
                "text": obj.name,
                "iconCls": "icon-object",
                "state": state,
                "children": variables

            })

        return children

    def get_vars(self, object_id):
        children = []
        variables = Var.query.filter_by(object_id=object_id).order_by(Var.id.asc()).all()
        for var in variables:
            children.append({
                "id": var.name,
                "text": var.name,
                "iconCls": "icon-var"
            })

        return children

    def get_keyword_suites(self, project_id):
        children = []
        suites = UserKeywordSuite.query.filter_by(project_id=project_id).order_by(
            UserKeywordSuite.id.asc()).all()

        for suite in suites:
            keywords = self.get_keywords(suite.id)
            if len(keywords) == 0:
                state = "open"
            else:
                state = "closed"
            children.append({
                "id": suite.name,
                "text": suite.name,
                "iconCls": "icon-user_keyword",
                "state": state,
                "children": keywords

            })

        return children

    def get_keywords(self, suite_id):
        children = []
        keywords = UserKeyword.query.filter_by(keyword_suite_id=suite_id).order_by(UserKeyword.id.asc()).all()
        for key in keywords:
            children.append({
                "id": key.keyword,
                "text": key.keyword,
                "iconCls": "icon-step"
            })

        return children
