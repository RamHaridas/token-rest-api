from db import db
from datetime import datetime
from pytz import timezone


class BookingModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer)  # branch id
    sid = db.Column(db.Integer)  # service id
    cid = db.Column(db.Integer)  # counter id
    slot = db.Column(db.Integer)  # slot id
    uid = db.Column(db.Integer)  # user id
    name = db.Column(db.String(length=None))
    branch = db.Column(db.String(length=None))
    service = db.Column(db.String(length=None))
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    added_on = db.Column(db.Date)
    pdf = db.Column(db.String(length=None))  # url of pdf

    def __init__(self, bid, sid, cid, slot, uid, name, start, end, service, branch):
        self.bid = bid
        self.sid = sid
        self.cid = cid
        self.uid = uid
        self.slot = slot
        self.name = name
        self.start = start
        self.end = end
        self.service = service
        self.branch = branch
        self.added_on = datetime.utcnow().astimezone(timezone('Asia/Kolkata')).date()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return{
            'id': self.id,
            'bid':self.bid,
            'sid':self.sid,
            'slot':self.slot,
            'uid':self.uid,
            'name': self.name,
            'start': self.start.strftime("%I.%M %p"),
            'end': self.end.strftime("%I.%M %p"),
            'service': self.service,
            'branch': self.branch,
            'added_on': str(self.added_on)
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, added_on=datetime.utcnow().astimezone(timezone('Asia/Kolkata')).date()).first()

    @classmethod
    def get_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid, added_on=datetime.utcnow().astimezone(timezone('Asia/Kolkata')).date()).all()

    @classmethod
    def get_by_uid_sid(cls, uid, sid):
        return cls.query.filter_by(uid=uid, sid=sid, added_on=datetime.utcnow().astimezone(timezone('Asia/Kolkata')).date()).first()

    @classmethod
    def get_by_service(cls, bid, sid):
        return cls.query.filter_by(bid=bid, sid=sid, added_on=datetime.utcnow().astimezone(timezone('Asia/Kolkata')).date()).all()

    @classmethod
    def get_by_branch(cls, bid):
        return cls.query.filter_by(bid=bid, added_on=datetime.utcnow().astimezone(timezone('Asia/Kolkata')).date()).all()
