from flask_app import db
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required


from models.user import User

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}


class UserResource(Resource):
    @jwt_required
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user, 200

    @marshal_with(user_fields)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        for key, value in args.items():
            if value:
                setattr(user, key, value)
        db.session.commit()
        return user, 200

    @jwt_required
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        user = User(username=args['username'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201
