from flask_restful import reqparse, Resource
from models.booking import BookingModel
from models.user import UserModel
from models.branch import BranchModel
from models.service import ServiceModel
from models.slot import SlotModel


class BookingResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('bid', type=int, required=True)
    parser.add_argument('sid', type=int, required=True)
    parser.add_argument('uid', type=int, required=True)
    parser.add_argument('cid', type=int, required=True)
    parser.add_argument('slot', type=int, required=True)

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.get_by_id(data['uid'])
        branch = BranchModel.get_by_id(data['bid'])
        service = ServiceModel.get_by_id(data['sid'])
        slot = SlotModel.get_by_id(data['slot'])
        bookings = BookingModel.get_by_service(data['bid'], data['sid'])
        if not user:
            return {'msg': 'User not found'}, 404
        elif not branch:
            return {'msg': 'Branch not found'}, 404
        elif not service:
            return {'msg': 'Service not found'}, 404
        elif not slot:
            return {'msg': 'Slot not found'}, 404
        elif slot.token <= 0:
            return {'msg': 'Sorry, No Slots Available'}, 400
        elif BookingModel.get_by_uid_sid(data['uid'], data['sid']):
            return {'msg': 'You have already booked a slot today'}, 400
        elif len(bookings) >= slot.token:
            return {'msg': 'No more slots available'}, 400

        data['name'] = user.name or ""
        data['start'] = slot.start or ""
        data['end'] = slot.end or ""
        data['service'] = service.name or ""
        data['branch'] = branch.name or ""
        book = BookingModel(**data)
        book.save()
        return book.json(), 200

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument('bid', type=int, required=False)
        local.add_argument('sid', type=int, required=False)
        local.add_argument('uid', type=int, required=False)
        #local.add_argument('cid', type=int, required=False)
        local.add_argument('id', type=int, required=False)
        data = local.parse_args()

        if data['sid'] and data['bid']:
            return {'bookings': [b.json() for b in BookingModel.get_by_service(data['bid'], data['sid'])]}, 200
        elif data['bid']:
            return {'bookings': [b.json() for b in BookingModel.get_by_branch(data['bid'])]}, 200
        elif data['uid']:
            return {'bookings': [b.json() for b in BookingModel.get_by_uid(data['uid'])]}, 200
        elif data['id']:
            book = BookingModel.get_by_id(data['id'])
            return book.json() if book else {'msg': "NOT FOUD"}, 200

        return {'bookings': [b.json() for b in BookingModel.query.all()]}, 200

    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument('id', type=int, required=False)
        data = local.parse_args()
        book = BookingModel.get_by_id(data['id'])
        slot = SlotModel.get_by_id(book.slot)
        if book:
            book.delete()
            return {'msg': 'Slot Deleted Successfully'}, 200

        return {'msg': 'Slot does not exist'}, 404
