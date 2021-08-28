from flask_restful import reqparse,Resource
from models.slot import SlotModel


class SlotResource(Resource):
    parser = reqparse.RequestParser()
    