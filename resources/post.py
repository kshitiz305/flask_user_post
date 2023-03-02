from flask_app import db
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import  jwt_required

from models.post import Post
from models.user import User
from resources.user import user_fields

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'user_id': fields.Integer,
    'likes': fields.List(fields.Nested(user_fields))
}



class PostResource(Resource):
    @marshal_with(post_fields)
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post, 200

    @jwt_required
    @marshal_with(post_fields)
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        args = parser.parse_args()
        for key, value in args.items():
            if value:
                setattr(post, key, value)
        db.session.commit()
        return post, 200

    @jwt_required
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


class PostListResource(Resource):
    @marshal_with(post_fields)
    def get(self):
        posts = Post.query.all()
        return posts, 200

    @jwt_required
    @marshal_with(post_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('user_id', type=int, required=True)
        args = parser.parse_args()
        post = Post(title=args['title'], content=args['content'], user_id=args['user_id'])
        db.session.add(post)
        db.session.commit()
        return post, 201

class PostLikeResource(Resource):
    @marshal_with(post_fields)
    def post(self, post_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        args = parser.parse_args()
        user = User.query.get_or_404(args['user_id'])
        post = Post.query.get_or_404(post_id)
        if user in post.likes:
            post.likes.remove(user)
        else:
            post.likes.append(user)
        db.session.commit()
        return post, 200

    @jwt_required
    def delete(self, post_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        args = parser.parse_args()
        post = Post.query.get_or_404(post_id)
        # user_id = get_jwt_identity()
        user = User.query.get_or_404(args['user_id'])
        if user in post.likes:
            post.likes.remove(user)
            db.session.commit()
        return '', 204