from models.service import ServiceModel
from flask_restful import reqparse,Resource


class ServiceResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True)
    parser.add_argument('bid',type=int,required=True)
    parser.add_argument('documents',type=str,required=True)


    def post(self):
        data = self.parser.parse_args()
        if ServiceModel.get_by_name_and_branch(data['name'],data['bid']):
            return {'msg':'Service with same name already exists'},400
        
        service = ServiceModel(**data)
        service.save()
        return service.json(),200

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=False)

        return {'msg':[s.json() for s in ServiceModel.get_all_services()]}

    
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        local.add_argument('name',type=str,required=False)
        local.add_argument('document',type=str,required=False)
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