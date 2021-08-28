from db import db
from datetime import time


class SlotModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    bid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    isBlocked = db.Column(db.Boolean,default=False)


    def __init__(self,start,end,bid,sid):
        self.start = start
        self.end = end
        self.bid = bid
        self.sid = sid


    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    def update(self,id,time,isBlocked):
        if time:
            self.time = time
        if isBlocked in [0,1]:
            self.isBlocked = True if isBlocked > 0 else False
        db.session.commit()
    

    def json(self):
        
        return {
            'id': self.id,
            'start':self.start.strftime("%I %p"),
            'end':self.end.strftime("%I %p"),
            'bid':self.bid,
            'sid':self.sid
        }

    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


    @classmethod
    def get_all_slots(cls,bid,sid):
        return cls.query.filter_by(sid=sid,bid=bid,isBlocked=False).all()


    