from flask_restful import Resource, reqparse


class Project(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('category', type=str)
        self.parser.add_argument('product_id', type=int)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('desc', type=str)
        self.parser.add_argument('version', type=str)
        self.parser.add_argument('tags', type=str)
        self.parser.add_argument('enable', type=bool, default=True)
        self.parser.add_argument('id', type=int, default=-1)
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('cron', type=str)
        self.parser.add_argument('setup', type=str)
        self.parser.add_argument('teardown', type=str)

        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('rows', type=int, default=15)

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
