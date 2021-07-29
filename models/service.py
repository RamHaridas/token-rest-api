from db import db

class ServiceModel(db.Model):
    __tablename__ = 'services_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=None))
    bid = db.Column(db.Integer)
    documents = db.Column(db.String(length=None))
    isBlocked = db.Column(db.Boolean,default=False)

    def __init__(self,name,bid,documents):
        self.name = name
        self.bid = bid
        self.documents = documents
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    def json(self):
        return{
            'id':self.id,
            'name':self.name,
            'bid':self.bid,
            'documents':self.documents,
        }

    def update(self,id,name,documents,isBlocked):
        if name:
            self.name = name
        if documents:
            self.documents = documents
        if isBlocked:
            self.isBlocked = True if isBlocked > 0 else False
        db.session.commit()
    
    
    @classmethod
    def get_all_services(cls,bid):
        return cls.query.filter_by(bid=bid,isBlocked=False).all()

    @classmethod
    def get_by_name_and_branch(cls, name, bid):
        return cls.query.filter_by(name=name,bid=bid).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()