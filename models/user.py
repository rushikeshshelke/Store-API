import sqlite3
from commonLibs.globalVariables import GlobalVariables
from commonLibs.database import db

class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id':self.id,
            'username':self.username
        }
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def findByUsername(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def findById(cls,_id):
        return cls.query.filter_by(id=_id).first()
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
