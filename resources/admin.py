from models.admin import AdminModel
from flask_restful import reqparse,Resource


class AdminResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True)
    parser.add_argument('email',type=str,required=True)
    parser.add_argument('password',type=str,required=True)
    parser.add_argument('designation',type=str,required=True)


    def post(self):
        data = self.parser.parse_args()

        if AdminModel.get_by_email(data['email']):
            return {'msg':'Email already registered with us'},400
        
        admin = AdminModel(**data)
        admin.save()
        return admin.json(),200

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=False)
        local.add_argument('email',type=str,required=False)
        local.add_argument('password',type=str,required=False)
        data = local.parse_args()
        admin = AdminModel.get_by_id(data['id'])
        if admin:
            return admin.json(),200
        admin = AdminModel.login(data['email'],data['password'])
        if admin:
            return admin.json(),200
        return {'msg':'Admin does not exist'},404
    

    def put(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        local.add_argument('name',type=str,required=False)
        local.add_argument('password',type=str,required=False)
        local.add_argument('designation',type=str,required=False)
        data = local.parse_args() 
        admin = AdminModel.get_by_id(data['id'])
        if admin:
            admin.update(**data)
            return admin.json(),200
        return {'msg':'ID does not exist'},404

    
    def delete(self):
        return "METHOD NOT FOUND",404