from flask_restful import reqparse, Resource
from models.appointment import AppointmentModel
from models.user import UserModel
from models.executives import ExecutiveModel


class AppointmentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('uid', type=int, required=True)
    parser.add_argument('eid', type=int, required=True)
    parser.add_argument('bid', type=int, required=True)
    parser.add_argument('reason',type=str, required=False)

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.get_by_id(data['uid'])
        exec = ExecutiveModel.get_by_id(data['eid'])

        if not user:
            return {'msg': 'User not found'}, 404
        elif not exec:
            return {'msg': 'Executive not found'}, 404
        try:
            data['user_name'] = user.name or ""
            data['user_email'] = user.email or ""
            data['designation'] = exec.designation or ""
            data['exec_name'] = exec.name or ""
            app = AppointmentModel(**data)
            app.save()
        except:
            return {'msg': 'Internl Server Error'}, 500

        return app.json(), 200

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('uid', type=int, required=False)
        local.add_argument('eid', type=int, required=False)
        local.add_argument('bid', type=int, required=False)
        local.add_argument('id', type=int, required=False)
        data = local.parse_args()
        if data['uid']:
            return {'appointments': [a.json() for a in AppointmentModel.get_by_uid(data['uid'])]}, 200
        elif data['eid']:
            return {'appointments': [a.json() for a in AppointmentModel.get_by_eid(data['eid'])]}, 200
        elif data['bid']:
            return {'appointments': [a.json() for a in AppointmentModel.get_by_branch(data['bid'])]}, 200
        elif data['id']:
            app = AppointmentModel.get_by_id(data['id'])
            if app:
                return app.json(), 200

        return {'msg': 'Appointment not found'}, 404
