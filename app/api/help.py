from flask_restful import Resource, reqparse

from app.utils.parsing import parser_doc


class HelpApi(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()

	def get(self):
		args = self.parser.parse_args()
		return parser_doc()
