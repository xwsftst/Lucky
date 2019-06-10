# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\WorkSpace\Lucky\app\api\keyword.py
# Size of source mod 2**32: 887 bytes
from flask_restful import Resource, reqparse
from app.models import Project
from app.utils.parsing import parser

class KeywordApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('project_id', type=int, default=(-1))

    def get(self):
        args = self.parser.parse_args()
        if args['project_id'] != -1:
            children = []
            project = Project.query.filter_by(id=(args['project_id'])).first()
            if project:
                children.extend(self.get_objects(project.id))
            keyword_list = [
             {'id':project.id, 
              'text':project.name, 
              'state':'closed', 
              'iconCls':'icon-project', 
              'children':children}]
            return keyword_list
        else:
            return parser()
# okay decompiling E:\WorkSpace\Lucky\app\api\__pycache__\keyword.cpython-37.pyc
