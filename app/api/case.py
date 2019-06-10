# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\WorkSpace\Lucky\app\api\case.py
# Size of source mod 2**32: 5333 bytes
from datetime import datetime
from flask_login import current_user
from flask_restful import Resource, reqparse
from sqlalchemy import and_
from app.ext import db
from app.models import Case, User

class CaseApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int)
        self.parser.add_argument('suite_id', type=int)
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
        pagination = Case.query.filter_by(suite_id=(args['suite_id'])).order_by(Case.id.asc()).paginate((args['page']),
          per_page=(args['rows']), error_out=False)
        cases = pagination.items
        data = {'total':pagination.total,  'rows':[]}
        for v in cases:
            data['rows'].append({'id':v.id, 
             'suite_id':v.suite_id, 
             'name':v.name, 
             'desc':v.desc, 
             'create_user':User.query.filter_by(id=(v.create_user_id)).first().username, 
             'create_timestamp':v.create_timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
             'update_user':User.query.filter_by(id=(v.update_user_id)).first().username, 
             'update_timestamp':v.update_timestamp.strftime('%Y-%m-%d %H:%M:%S')})

        return data

    def post(self):
        args = self.parser.parse_args()
        method = args['method'].lower()
        if method == 'create':
            return (
             self._CaseApi__create(args), 201)
        elif method == 'edit':
            return (self._CaseApi__edit(args), 201)
        elif method == 'delete':
            return (self._CaseApi__delete(args), 201)
        elif method == 'query':
            return (self._CaseApi__query(args), 201)
        else:
            return (
             {'status':'fail', 
              'msg':'方法: %s 不支持' % method}, 201)

    def __create(self, args):
        result = {'status':'success', 
         'msg':'操作成功'}
        case = Case.query.filter(and_(Case.name == args['name'], Case.suite_id == args['suite_id'])).first()
        if case is None:
            try:
                case = Case(name=(args['name']), desc=(args['desc']),
                  suite_id=(args['suite_id']),
                  tags=(args['tags']),
                  enable=(args['enable']),
                  setup=(args['setup']),
                  teardown=(args['teardown']),
                  create_user_id=(current_user.get_id()),
                  update_user_id=(current_user.get_id()))
                db.session.add(case)
                db.session.commit()
                result['suite_id'] = case.suite_id
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '异常：%s' % str(e)
                finally:
                    e = None
                    del e

        else:
            result['status'] = 'fail'
            result['msg'] = '用例名称[%s]重复' % args['name']
        return result

    def __edit(self, args):
        result = {'status':'success', 
         'msg':'操作成功'}
        case = Case.query.filter_by(id=(args['id'])).first()
        if case is None:
            result['status'] = 'fail'
            result['msg'] = '未找到要修改的用例id'
        else:
            try:
                case.name = args['name']
                case.desc = args['desc']
                case.tags = args['tags']
                case.enable = args['enable']
                case.setup = args['setup']
                case.teardown = args['teardown']
                case.update_user_id = current_user.get_id()
                case.update_timestamp = datetime.now()
                db.session.merge(case)
                db.session.commit()
                result['suite_id'] = case.suite_id
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '编辑用例[id-%s]失败：%s' % (args['id'], str(e))
                finally:
                    e = None
                    del e

            return result

    def __delete(self, args):
        result = {'status':'success',  'msg':'操作成功'}
        case = Case.query.filter_by(id=(args['id'])).first()
        if case is None:
            result['status'] = 'fail'
            result['msg'] = '未找到要删除的用例id'
        else:
            try:
                result['suite_id'] = case.suite_id
                db.session.delete(case)
                db.session.commit()
            except Exception as e:
                try:
                    result['status'] = 'fail'
                    result['msg'] = '删除用例[id-%s]失败：%s' % (args['id'], str(e))
                finally:
                    e = None
                    del e

            return result
# okay decompiling E:\WorkSpace\Lucky\app\api\__pycache__\case.cpython-37.pyc
