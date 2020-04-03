from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find(name)
        if store:
            return store.json()
        return {"message": 'Store not found'},400

    def post(self,name):
        if StoreModel.find(name):
            return {'message':"A store '{}' already exists".format(name)},400
        store = StoreModel(name)
        try:
            store.save()
        except:
            return {"message":"Failed to create '{}' store".format(name)},500
        return {"message":"Store '{}' was created.".format(name)},201

    def delete(self,name):
        store = StoreModel.find(name)
        if store:
            if not store.delete():
                return {"message":"Failed to delete '{}' store".format(name)},500
        return {"message":"Store '{}' was deleted".format(name)}

class StoreList(Resource):
    def get(self):
        return {"stores":[store.json() for store in StoreModel.query.all()]}