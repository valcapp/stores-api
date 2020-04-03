from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self,name):
        item = ItemModel.find(name)
        if item:
            return {'item':item.json()}, 200
        else:
            return {'message': "Item '{}' not found".format(name)}, 404

    def post(self, name):
        if ItemModel.find(name):
            return {'message':"Item '{}' already exists".format(name)}, 400
        failed = {"message":"Failed to create '{}' item.".format(name)},500
        data = Item.parser.parse_args()
        item = ItemModel(name,**data)
        try:
            if item.save():
                return {'message':"Item '{}' created.".format(name),'item':item.json()},201
            else:
                return failed
        except:
            return failed
    
    def put(self,name):
        data = Item.parser.parse_args()
        failed = {"message":"Failed to update '{}' item.".format(name)}
        
        item = ItemModel.find(name)        
        try:
            if item:
                item.price = data['price']
                item.store_id = data['store_id']
            else:
                item = ItemModel(name,**data)
            if not item.save():
                return failed
            return {'message':"Item '{}' updated ".format(name),'item':item.json()},200
        except:
            return failed
    
    def delete(self, name):
        item = ItemModel.find(name)
        failed = {"message":"Failed to delete '{}' item.".format(name)},500
        try:
            if item:
                item.delete()
        except:
            return failed
        if ItemModel.find(name):
            return failed
        else:
            return {'message':"Item '{}' deleted".format(name)},200


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {'items':list(map(lambda i: i.json(),items))},200
        