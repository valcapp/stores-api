from flask_restful import Resource, reqparse

from db import db
from models.user import User

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message':"A username '{}' already exists.".format(data['username'])},400

        user = User(**data)
        user.save()
        
        return {"message":"User created successfully."},201

