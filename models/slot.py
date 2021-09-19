from db import db
from datetime import time
from sqlalchemy import asc


class SlotModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    bid = db.Column(db.Integer)
    token = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    isBlocked = db.Column(db.Boolean, default=False)

    def __init__(self, start, end, bid, sid, token):
        self.start = start
        self.end = end
        self.bid = bid
        self.sid = sid
        self.token = token

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, id, start, end, token, isBlocked):
        if token:
            self.token = token
        if start:
            self.start = start
        if end:
            self.end = end
        if isBlocked in [0, 1]:
            self.isBlocked = True if isBlocked > 0 else False
        db.session.commit()

    # def bookSlot(self):
    #     self.token = self.token - 1
    #     db.session.commit()

    # def releaseSlot(self):
    #     self.token = self.token + 1
    #     db.session.commit()

    def json(self):

        return {
            'id': self.id,
            'start': self.start.strftime("%I.%M %p"),
            'end': self.end.strftime("%I.%M %p"),
            'bid': self.bid,
            'sid': self.sid,
            'tokens': self.token,
            'isBlocked': self.isBlocked
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_slots(cls, bid, sid):
        return cls.query.filter_by(sid=sid, bid=bid).order_by(asc(cls.start)).all()
