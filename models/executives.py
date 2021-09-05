from db import db
import json


class ExecutiveModel(db.Model):
    __tablename__ = 'exec_tbl'
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer)
    name = db.Column(db.String(length=None))
    designation = db.Column(db.String(length=None))
    mobile = db.Column(db.String(length=None))
    email = db.Column(db.String(length=None))

    def __init__(self, bid, name, designation, email, mobile):
        self.name = name
        self.bid = bid
        self.designation = designation
        if email:
            self.email = email
        if mobile:
            self.mobile = mobile

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation,
            'mobile': self.mobile or "",
            'email': self.email or "",
            'bid': self.bid
        }

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_branch(cls, bid):
        return cls.query.filter_by(bid=bid).all()
