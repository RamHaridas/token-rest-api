from models.branch import BranchModel
from models.service import ServiceModel
from models.executives import ExecutiveModel
from flask_restful import reqparse,Resource


class ServiceResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True)
    parser.add_argument('bid',type=int,required=True)
    parser.add_argument('documents',type=str,required=True)


    def post(self):
        data = self.parser.parse_args()
        if not BranchModel.get_by_id(data['bid']):
            return {'msg':'Branch does not exist'},404
        
        if ServiceModel.get_by_name_and_branch(data['name'],data['bid']):
            return {'msg':'Service with same name already exists'},400
        
        service = ServiceModel(**data)
        service.save()
        return service.json(),200

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=False)
        local.add_argument('bid', type=int,required=False)
        data = local.parse_args()
        if data['id']:
            service = ServiceModel.get_by_id(data['id'])
            if not service:
                return {"msg":"Service not found"},404
            return service.json(),200
        
        return {
            'services':[s.json() for s in ServiceModel.get_all_services(data['bid'])],
            'executives': [e.json() for e in ExecutiveModel.get_by_branch(data['bid'])]
        },200

    
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        local.add_argument('name',type=str,required=False)
        local.add_argument('documents',type=str,required=False)
        local.add_argument('isBlocked',type=int,required=False)

        data = local.parse_args()
        service = ServiceModel.get_by_id(data['id'])
        if not service:
            return {'msg':'service not found'},404
        
        service.update(**data)
        return service.json(),200


    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        data = local.parse_args()
        service = ServiceModel.get_by_id(data['id'])
        if service:
            service.delete()
            return {'msg': 'Service deleted'},200

        return {'msg': 'Service not found'},404