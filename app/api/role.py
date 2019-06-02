from flask_restful import Resource

from app.models import Role


class RoleApi(Resource):
    def __init__(self):
        pass

    def get(self):
        data = {"rows": []}
        roles = Role.query.all()
        for r in roles:
            data["rows"].append({
                "id": r.id,
                "name": r.name
            })

        return data