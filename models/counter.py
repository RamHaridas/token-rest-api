from db import db

class CounterModel(db.Model):
    __tablename__ = 'counter_tbl'
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    no = db.Column(db.String(length=None))
    isBlocked = db.Column(db.Boolean,default=False)


    def __init__(self,no,bid,sid):
        self.no = no
        self.bid = bid
        self.sid = sid
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    def json(self):
        return {"id":self.id,"number":self.no,"isBlocked":self.isBlocked}

    
    def update(self,id,no,isBlocked):
        if no:
            self.no = no
        if isBlocked:
            self.isBlocked = True if isBlocked > 0 else False
        db.session.commit()

    

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_number(cls, number,bid):
        return cls.query.filter_by(no=number,bid=bid).first()
    
    @classmethod
    def get_all_counters(cls,bid,sid):
        return cls.query.filter_by(sid=sid,bid=bid).all()