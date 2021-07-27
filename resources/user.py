from flask_restful import Resource,reqparse
from models.user import UserModel


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('guid',type=str,required=True)
    parser.add_argument('name',type=str,required=True)
    parser.add_argument('image',type=str,required=True)
    parser.add_argument('email',type=str,required=True)



    def post(self):
        data = self.parser.parse_args()

        user = UserModel.get_by_guid(data['guid'])
        if user:
            return user.json(),200
        
        user = UserModel(**data)
        user.save()
        return user.json(),200

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        data = local.parse_args()
        user = UserModel.get_by_id(data['id'])
        if user:
            return user.json(),200
        
        return {'msg':'User not found'},404

    
    def delte(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        data = local.parse_args()
        user = UserModel.get_by_id(data['id'])
        if user:
            user.delete()
            return {'msg':'Account deleted successfully'},200
        
        return {'msg':'User not found'},404