from models.counter import CounterModel
from models.branch import BranchModel
from flask_restful import reqparse,Resource


class CounterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('no',type=str,required=True)
    parser.add_argument('bid',type=int,required=True)
    parser.add_argument('sid',type=int,required=True)


    def post(self):
        data = self.parser.parse_args()

        if not BranchModel.get_by_id(data['bid']):
            return {'msg':'Branch does not exist'},404
        
        counter = CounterModel(**data)
        counter.save()
        return counter.json(),200
    

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('bid', type=int,required=True)
        local.add_argument('sid', type=int,required=True)
        data = local.parse_args()

        return {'counters':[c.json() for c in CounterModel.get_all_counters(**data)]}


    def put(self):
        local = reqparse.RequestParser()
        local.add_argument('no', type=str,required=False)
        local.add_argument('id', type=int,required=True)
        local.add_argument('isBlocked', type=int,required=False)
        data = local.parse_args()

        counter = CounterModel.get_by_id(data['id'])
        if not counter:
            return {'msg':'Counter not found'},404
        
        counter.update(**data)
        return counter.json(),200

    
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=True)
        data = local.parse_args()
        counter = CounterModel.get_by_id(data['id'])
        if counter:
            counter.delete()
            return {'msg': 'Counter deleted'},200

        return {'msg': 'Counter not found'},404