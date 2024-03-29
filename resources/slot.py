from flask_restful import reqparse, Resource
from models.slot import SlotModel
from datetime import datetime, time


class SlotResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('start', type=str, required=True)
    parser.add_argument('end', type=str, required=True)
    parser.add_argument('bid', type=int, required=True)
    parser.add_argument('sid', type=int, required=True)
    parser.add_argument('token', type=int, required=True)

    # @desc to save slot data
    def post(self):
        data = self.parser.parse_args()
        try:
            start = datetime.strptime(data['start'], '%H:%M:%S')
            data['start'] = start
            end = datetime.strptime(data['end'], '%H:%M:%S')
            data['end'] = end
        except:
            return {'msg': 'Invalid Time Format'}, 400
        slot = SlotModel(**data)
        slot.save()
        return slot.json(), 200
        # end


    # @desc to get slot list based on branch and service
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int,required=False)
        local.add_argument('bid', type=int, required=False)
        local.add_argument('sid', type=int, required=False)
        local.add_argument('time', type=str, required=False)
        data = local.parse_args()
        if data['id']:
            slot = SlotModel.get_by_id(data['id'])
            if not slot:
                return {'msg': 'Slot not found'},404
            return slot.json(), 200
        if data['time']:
            try:
                start = datetime.strptime(data['time'], '%H:%M:%S')
            except:
                return {'msg': 'Invalid Time Format'}, 400
            slots = []
            for slot in SlotModel.get_all_slots(data['bid'], data['sid']):
                if slot.start > start.time():
                    slots.append(slot.json())
            return {'slots': slots}, 200
        return {'slots': [s.json() for s in SlotModel.get_all_slots(data['bid'], data['sid'])]}, 200
        # end


    # @desc to delete a slot
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int, required=True)
        #local.add_argument('sid', type=int, required=True)
        data = local.parse_args()
        slot = SlotModel.get_by_id(data['id'])
        if slot:
            slot.delete()
            return {'msg': 'Slot deleted successfully'}, 200

        return {'msg': 'Slot not found'}, 404
        # end

    # @desc update slot details
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int, required=True)
        local.add_argument('start', type=str, required=False)
        local.add_argument('end', type=str, required=False)
        local.add_argument('token', type=int, required=False)
        local.add_argument('isBlocked', type=int, required=False)
        data = local.parse_args()
        slot = SlotModel.get_by_id(data['id'])
        if data['start']:
            try:
                start = datetime.strptime(data['start'], '%H:%M:%S')
                data['start'] = start
            except:
                return {'msg': 'Invalid Time Format, Valid Format is hh:mm:ss (24 hour clock)'}, 400
        if data['end']:
            try:
                end = datetime.strptime(data['end'], '%H:%M:%S')
                data['end'] = end
            except:
                return {'msg': 'Invalid Time Format, Valid Format is hh:mm:ss (24 hour clock)'}, 400
        if slot:
            slot.update(**data)
            return slot.json(), 200
        return {'msg': 'Slot not found'}, 404
        # end
