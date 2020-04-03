from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {'name':self.name, 'price':self.price, 'store_id':self.store_id}

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