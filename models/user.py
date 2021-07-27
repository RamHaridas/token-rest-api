from db import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'token_users_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=None))
    email = db.Column(db.String(length=None))
    guid = db.Column(db.String(length=None))
    image = db.Column(db.String(length=None))
    isBlocked = db.Column(db.Boolean,default=False)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)


    def __init__(self,name,guid,email,image):
        self.name = name
        self.guid = guid
        self.email = email
        self.image = image


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
            'email':self.email,
            'guid':self.guid,
            'isBlocked':self.isBlocked,
            'image':self.image,
        }


    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


    @classmethod
    def get_by_guid(cls, guid):
        return cls.query.filter_by(guid=guid).first()

    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()