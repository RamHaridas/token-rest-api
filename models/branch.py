from db import db
from sqlalchemy.sql.expression import false

class BranchModel(db.Model):
    __tablename__ = 'token_branch_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=None))
    ifsc = db.Column(db.String(length=None))
    address = db.Column(db.String(length=None))
    image = db.Column(db.String(length=None))
    isBlocked = db.Column(db.Boolean,default=False)


    def __init__(self,name,ifsc):
        self.name = name
        self.ifsc = ifsc


    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    def json(self):
        return {
            'id':self.id,
            'name':self.name,
            'ifsc':self.ifsc,
            'isBlocked':self.isBlocked,
        }
    

    def update(self,id,name,ifsc,isBlocked):
        if name:
            self.name = name
        if ifsc:
            self.ifsc = ifsc
        if isBlocked:
            self.isBlocked = True if isBlocked > 0 else False
        db.session.commit()


    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    
    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    
    @classmethod
    def get_by_ifsc(cls, ifsc):
        return cls.query.filter_by(ifsc=ifsc).first()

    @classmethod
    def get_all_branches(cls):
        return cls.query.filter_by(isBlocked=False).all()