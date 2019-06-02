from datetime import datetime

from flask_login import current_user
from flask_restful import Resource, reqparse

from app.ext import db
from app.models import Product, User


class ProductApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, default=-1)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('desc', type=str)
        self.parser.add_argument('tags', type=str)
        self.parser.add_argument('enable', type=bool, default=True)
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('rows', type=int, default=15)

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

    def get(self):
        args = self.parser.parse_args()

        pagination = Product.query.order_by(Product.id.desc()).paginate(
            args["page"], per_page=args["rows"],
            error_out=False
        )

        products = pagination.items
        data = {"total": pagination.total, "rows": []}
        status = {True: "激活", False: "不可用"}
        for p in products:
            data["rows"].append({
                "id": p.id,
                "name": p.name,
                "desc": p.desc,
                "enable": status[p.enable],
                "create_user": User.query.filter_by(id=p.create_user_id).first().username,
                "create_timestamp": p.create_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "update_user": User.query.filter_by(id=p.update_user_id).first().username,
                "update_timestamp": p.update_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })

        return data

    def __create(self, args):
        result = {"status": "success",
                  "msg": "操作成功"}
        # print(args)
        product = Product.query.filter_by(name=args["name"]).first()
        if product is None:
            try:
                product = Product(name=args["name"],
                                  desc=args["desc"],
                                  tags=args["tags"],
                                  enable=args["enable"],
                                  create_user_id=current_user.get_id(),
                                  update_user_id=current_user.get_id())
                db.session.add(product)
                db.session.commit()
            except Exception as e:
                result["status"] = "fail"
                result["msg"] = "异常：%s" % str(e)
        else:
            result["status"] = "fail"
            result["msg"] = "产品名称[%s]重复" % args["name"]

        return result

    def __query(self, args):
        data = {"rows": []}
        if args["id"] == -1:
            # 详细信息
            status = {True: "激活", False: "不可用"}
            products = Product.query.all()
            for p in products:
                data["rows"].append({
                    "id": p.id,
                    "name": p.name,
                    "desc": p.desc,
                    "enable": status[p.enable],
                    "create_user": User.query.filter_by(id=p.create_user_id).first().username,
                    "create_timestamp": p.create_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "update_user": User.query.filter_by(id=p.update_user_id).first().username,
                    "update_timestamp": p.update_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                })
        elif args["id"] == -2:
            # 简略信息
            products = Product.query.filter_by(enable=True).all()
            for p in products:
                data["rows"].append({
                    "id": p.id,
                    "name": p.name
                })

        return data

    def __edit(self, args):
        result = {"status": "success",
                  "msg": "操作成功"}

        product = Product.query.filter_by(id=args["id"]).first()
        if product is None:
            result["status"] = "fail"
            result["msg"] = "未找到要修改的产品id"
        else:
            try:
                product.name = args["name"]
                product.desc = args["desc"]
                product.tags = args["tags"]
                product.enable = args["enable"]
                product.update_user_id = current_user.get_id()
                product.update_timestamp = datetime.now()

                db.session.merge(product)
                db.session.commit()
            except Exception as e:
                result["status"] = "fail"
                result["msg"] = "编辑产品[id-%s]失败：%s" % (args["id"], str(e))

        return result

    def __delete(self, args):
        result = {"status": "success",
                  "msg": "操作成功"}

        product = Product.query.filter_by(id=args["id"]).first()
        if product is None:
            result["status"] = "fail"
            result["msg"] = "未找到要删除的产品id"
        else:
            try:
                db.session.delete(product)
                db.session.commit()
            except Exception as e:
                result["status"] = "fail"
                result["msg"] = "删除产品[id-%s]失败：%s" % (args["id"], str(e))

        return result
