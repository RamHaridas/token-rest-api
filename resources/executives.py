from flask_restful import reqparse, Resource
from models.executives import ExecutiveModel
import werkzeug
from firebase import FireBaseService


class ExcecutiveResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('designation', type=str, required=True)
    parser.add_argument('mobile', type=str, required=False)
    parser.add_argument('email', type=str, required=False)
    parser.add_argument('image', type=werkzeug.datastructures.FileStorage, required=False,location='files')
    parser.add_argument('bid', type=int, required=True)

    def post(self):
        data = self.parser.parse_args()
        file = data['image']
        if file:
            fb = FireBaseService()
            data['image'] = fb.uploadFile(file)
        
        exec = ExecutiveModel(**data)
        exec.save()
        return exec.json(), 200

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('bid', type=int, default=False)
        local.add_argument('id', type=int, default=False)
        data = local.parse_args()
        if data['bid']:
            return {'executives': [e.json() for e in ExecutiveModel.get_by_branch(data['bid'])]}, 200
        elif data['id']:
            exec = ExecutiveModel.get_by_id(data['id'])
            if exec:
                return exec.json(), 200

        return {'msg': 'Not found'}, 404
