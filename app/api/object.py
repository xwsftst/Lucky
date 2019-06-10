# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\WorkSpace\Lucky\app\api\object.py
# Size of source mod 2**32: 5558 bytes
from datetime import datetime
from flask_login import current_user
from flask_restful import Resource, reqparse
from sqlalchemy import and_
from app.ext import db
from app.models import Object, User

class ObjectApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, default=(-1))
        self.parser.add_argument('project_id', type=int)
        self.parser.add_argument('category', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('desc', type=str)
        self.parser.add_argument('tags', type=str)
        self.parser.add_argument('prev', type=int)
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('enable', type=bool, default=True)
        self.parser.add_argument('setup', type=str)
        self.parser.add_argument('teardown', type=str)
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('rows', type=int, default=15)

    def get(self):
        args = self.parser.parse_args()
        pagination = Object.query.filter_by(project_id=(args['project_id'])).order_by(Object.id.asc()).paginate((args['page']),
          per_page=(args['rows']), error_out=False)
        objects = pagination.items
        data = {'total':pagination.total,  'rows':[]}
        for o in objects:
            data['rows'].append({'id':o.id, 
             'project_id':o.project_id, 
             'name':o.name, 
             'desc':o.desc, 
             'create_user':User.query.filter_by(id=(o.create_user_id)).first().username, 
             'create_timestamp':o.create_timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
             'update_user':User.query.filter_by(id=(o.update_user_id)).first().username, 
             'update_timestamp':o.update_timestamp.strftime('%Y-%m-%d %H:%M:%S')})

        return data

    def post(self):
        args = self.parser.parse_args()
        method = args['method'].lower()
        if method == 'create':
            return (
             self._ObjectApi__create(args), 201)
        elif method == 'edit':
            return (self._ObjectApi__edit(args), 201)
        elif method == 'delete':
            return (self._ObjectApi__delete(args), 201)
        elif method == 'query':
            return (self._ObjectApi__query(args), 201)
        else:
            return (
             {'status':'fail', 
              'msg':'方法: %s 不支持' % method}, 201)

    def __create(self, args):
        result = {'status':'success', 
         'project_id':args['project_id'],  'msg':'操作成功'}
        suite = Object.query.filter(and_(Object.name == args['name'], Object.project_id == args['project_id'])).first()
        if suite is None:
            try:
                suite = Object(name=(args['name']), desc=(args['desc']),
                  project_id=(args['project_id']),
                  tags=(args['tags']),
                  category=(args['category']),
                  enable=(args['enable']),
                  setup=(args['setup']),
                  teardown=(args['teardown']),
                  create_user_id=(current_user.get_id()),
                  update_user_id=(current_user.get_id()))
                db.session.add(suite)
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
            result['msg'] = '对象集名称[%s]重复' % args['name']
        return result

    def __edit(self, args):
        result = {'status':'success', 
         'msg':'操作成功'}
        suite = Object.query.filter_by(id=(args['id'])).first()
        if suite is None:
            result['status'] = 'fail'
            result['msg'] = '未找到要修改的对象集id'
        else:
            try:
                suite.name = args['name']
                suite.desc = args['desc']
                suite.tags = args['tags']
                suite.enable = args['enable']
                suite.setup = args['setup']
                suite.teardown = args['teardown']
                suite.update_user_id = current_user.get_id()
                suite.update_timestamp = datetime.now()
                db.session.merge(suite)
                db.session.commit()
                result['project_id'] = suite.project_id
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '编辑对象集[id-%s]失败：%s' % (args['id'], str(e))
                finally:
                    e = None
                    del e

            return result

    def __delete(self, args):
        result = {'status':'success',  'msg':'操作成功'}
        suite = Object.query.filter_by(id=(args['id'])).first()
        if suite is None:
            result['status'] = 'fail'
            result['msg'] = '未找到要删除的对象集id'
        else:
            try:
                result['project_id'] = suite.project_id
                db.session.delete(suite)
                db.session.commit()
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '删除对象集[id-%s]失败：%s' % (args['id'], str(e))
                finally:
                    e = None
                    del e

            return result
# okay decompiling E:\WorkSpace\Lucky\app\api\__pycache__\object.cpython-37.pyc
