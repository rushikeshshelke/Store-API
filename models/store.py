from commonLibs.database import db

class StoreModel(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel',lazy='dynamic')

    def __init__(self,name):
        self.name = name
    
    def json(self):
        return {
                'id': self.id,
                'name':self.name,
                'items':[item.json() for item in self.items.all()]
            }

    @classmethod
    def select(cls,storeName):
        return cls.query.filter_by(name=storeName).first()

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def findAll(cls):
        return cls.query.all()