from flask_restful import reqparse,Resource
from models.branch import BranchModel


class BranchResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True)
    parser.add_argument('ifsc',type=str,required=True)

    def post(self):
        data = self.parser.parse_args()
        if BranchModel.get_by_name(data['name']):
            return {'msg':'Branch with same name already exists'},400
        
        branch = BranchModel(**data)
        branch.save()
        return branch.json(),200

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        data = local.parse_args()
        branch = BranchModel.get_by_id(data['id'])
        if branch:
            return branch.json(),200
        
        return {'branch':[b.json() for b in BranchModel.query.all()]},200

    
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        data = local.parse_args()
        branch = BranchModel.get_by_id(data['id'])
        if branch:
            branch.delete()
            return {'msg':'Branch deleted'},200
        
        return {'msg':'Branch not found'},404
    
    