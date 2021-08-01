from db import db


class AdminModel(db.Model):
    __tablename__ = 'admin_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=None))
    email = db.Column(db.String(length=None))
    password = db.Column(db.String(length=None))
    designation = db.Column(db.String(length=None))


    def __init__(self,name,email,password,designation):
        self.name = name
        self.email = email
        self.password = password
        self.designation = designation

    
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
            'email':self.email,
            'designation':self.designation
        }
    
    def update(self,id,name,password,designation):
        if name:
            self.name = name
        if password:
            self.password = password
        if designation:
            self.designation = designation
        db.session.commit()
    

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def login(cls,email,password):
        return cls.query.filter_by(email=email,password=password).first()