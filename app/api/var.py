# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\WorkSpace\Lucky\app\api\var.py
# Size of source mod 2**32: 5494 bytes
from datetime import datetime
from flask_login import current_user
from flask_restful import reqparse, Resource
from sqlalchemy import and_
from app.ext import db
from app.models import Object, Var, User

class VarApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int)
        self.parser.add_argument('object_id', type=int, default=(-1))
        self.parser.add_argument('desc', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('value', type=str)
        self.parser.add_argument('category', type=str, default='var')
        self.parser.add_argument('prev', type=int)
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('rows', type=int, default=15)

    def get(self):
        args = self.parser.parse_args()
        pagination = Var.query.filter_by(object_id=(args['object_id'])).order_by(Var.id.asc()).paginate((args['page']),
          per_page=(args['rows']), error_out=False)
        vars = pagination.items
        data = {'total':pagination.total,  'rows':[]}
        for v in vars:
            data['rows'].append({'id':v.id, 
             'object_id':v.object_id, 
             'name':v.name, 
             'desc':v.desc, 
             'value':v.value, 
             'create_user':User.query.filter_by(id=(v.create_user_id)).first().username, 
             'create_timestamp':v.create_timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
             'update_user':User.query.filter_by(id=(v.update_user_id)).first().username, 
             'update_timestamp':v.update_timestamp.strftime('%Y-%m-%d %H:%M:%S')})

        return data

    def post(self):
        args = self.parser.parse_args()
        import json
        method = args['method'].lower()
        if method == 'create':
            return (
             self._VarApi__create(args), 201)
        elif method == 'edit':
            return (self._VarApi__edit(args), 201)
        elif method == 'delete':
            return (self._VarApi__delete(args), 201)
        elif method == 'query':
            return (self._VarApi__query(args), 201)
        else:
            return (
             {'status':'fail', 
              'msg':'方法: %s 不支持' % method}, 201)

    def __create(self, args):
        result = {'status':'success', 
         'msg':'操作成功'}
        a_object = Object.query.filter_by(id=(args['object_id'])).first()
        if a_object is not None:
            project_id = a_object.project_id
            objs = Object.query.filter_by(project_id=project_id).all()
            for obj in objs:
                var = Var.query.filter(and_(Var.name == args['name'], Var.object_id == obj.id)).first()
                if var is not None:
                    result['status'] = 'fail'
                    result['msg'] = '变量名[%s]重复' % args['name']

        var = Var.query.filter(and_(Var.name == args['name'], Var.object_id == args['object_id'])).first()
        if var is None:
            try:
                var = Var(name=(args['name']), value=(args['value']),
                  desc=(args['desc']),
                  category=(args['category']),
                  object_id=(args['object_id']),
                  prev=(args['prev']),
                  create_user_id=(current_user.get_id()),
                  update_user_id=(current_user.get_id()))
                db.session.add(var)
                db.session.commit()
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '异常：%s' % str(e)
                finally:
                    e = None
                    del e

        else:
            result['status'] = 'fail'
            result['msg'] = '变量名[%s]重复' % args['name']
        return result

    def __edit(self, args):
        result = {'status':'success', 
         'msg':'操作成功'}
        var = Var.query.filter_by(id=(args['id'])).first()
        if var is None:
            result['status'] = 'fail'
            result['msg'] = '未找到要修改的变量id'
        else:
            try:
                var.name = args['name']
                var.value = args['value']
                var.desc = args['desc']
                var.update_user_id = current_user.get_id()
                var.update_timestamp = datetime.utcnow()
                db.session.merge(var)
                db.session.commit()
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '编辑变量[id-%s]失败：%s' % (args['id'], str(e))
                finally:
                    e = None
                    del e

            return result

    def __delete(self, args):
        result = {'status':'success',  'msg':'操作成功'}
        var = Var.query.filter_by(id=(args['id'])).first()
        if var is None:
            result['status'] = 'fail'
            result['msg'] = '未找到要删除的变量id'
        else:
            try:
                db.session.delete(var)
                db.session.commit()
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '删除变量[id-%s]失败：%s' % (args['id'], str(e))
                finally:
                    e = None
                    del e

            return result
# okay decompiling E:\WorkSpace\Lucky\app\api\__pycache__\var.cpython-37.pyc
