from models.executives import ExecutiveModel
from db import db
from datetime import datetime
from pytz import timezone


class AppointmentModel(db.Model):
    __tablename__ = 'appointment_tbl'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    eid = db.Column(db.Integer)
    bid = db.Column(db.Integer)
    user_name = db.Column(db.String(length=None))
    user_email = db.Column(db.String(length=None))
    exec_name = db.Column(db.String(length=None))
    designation = db.Column(db.String(length=None))
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    added_on = db.Column(db.Date)
    approved = db.Column(db.Integer)
    reason = db.Column(db.String(length=None))
    pdf = db.Column(db.String(length=None))

    def __init__(self, uid, eid, bid, user_name, user_email, exec_name, designation,reason):
        self.uid = uid
        self.eid = eid
        self.user_email = user_email
        self.bid = bid
        self.user_name = user_name
        self.designation = designation
        self.exec_name = exec_name
        if reason:
            self.reason = reason
        self.added_on = datetime.utcnow().astimezone(timezone('Asia/Kolkata')).date()

    def approve(self, approve, start, added_on):
        if approve == 1:
            self.approved = 1
            self.start = start
            if added_on:
                self.added_on = added_on
        elif approve == 0:
            self.approved = 0
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        status = "Pending for approval"
        image = ""
        exec = ExecutiveModel.get_by_id(self.eid)
        if exec:
            image = exec.image or ""
        if self.approved == 1:
            status = 'Approved'
        elif self.approved == 0:
            status = 'Rejected'

        return {
            'id': self.id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'uid': self.uid,
            'eid': self.eid,
            'bid': self.bid,
            'exec_name': self.exec_name,
            'designation': self.designation,
            'start': self.start.strftime("%I.%M %p") if self.start else "",
            'end': self.end.strftime("%I.%M %p") if self.end else "",
            'added_on': str(self.added_on),
            'approved': status,
            'reason': self.reason or "",
            'pdf': self.pdf or "",
            "image":image
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_branch(cls, bid):
        return cls.query.filter_by(bid=bid).all()

    @classmethod
    def get_by_eid(cls, eid):
        return cls.query.filter_by(eid=eid).all()

    @classmethod
    def get_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).all()
