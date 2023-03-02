from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('User', secondary='post_likes')

    def __repr__(self):
        return f"Post(title={self.title}, content={self.content}, user_id={self.user_id})"


post_likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'user_id': fields.Integer,
    'likes': fields.List(fields.Nested(user_fields))
}


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user, 200

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        for key, value in args.items():
            if value:
                setattr(user, key, value)
        db.session.commit()
        return user, 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()
        user = User(username=args['username'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201


class PostResource(Resource):
    @marshal_with(post_fields)
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post, 200

    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        args = parser.parse_args()
        for key, value in args.items:
            if value:
                setattr(post, key, value)
            db.session.commit()
            return post, 200

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

api.add_resource(UserResource, '/users/int:user_id')
api.add_resource(UserListResource, '/users')
api.add_resource(PostResource, '/posts/int:post_id')
api.add_resource(PostListResource, '/posts')
api.add_resource(PostLikeResource, '/posts/int:post_id/like')

if __name__ == '__main__':
    app.run(debug=True)