from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel',lazy='dynamic')

    def __init__(self,name):
        self.name = name
    
    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find(cls,name):
        # what if it doesn't find it?
        return cls.query.filter_by(name=name).first() # SELECT * FROM 'items' WHERE name=name LIMIT 1

    def save(self):
        db.session.add(self)
        db.session.commit()
        if self.find(self.name):
            return True

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        if self.find(self.name):
            return False