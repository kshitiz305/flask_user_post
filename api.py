# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
# db = SQLAlchemy(app)
# api = Api(app)
from resources.post import *
from resources.user import *
from ext import db

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask import Flask
from datetime import timedelta


def register_extensions(app):
    db.init_app(app)
    db.create_all(app=app)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)


    api = Api(app)
    jwt = JWTManager(app)
    register_extensions(app)


    api.add_resource(UserResource, '/users/int:user_id')
    api.add_resource(UserListResource, '/users')
    api.add_resource(PostResource, '/posts/int:post_id')
    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostLikeResource, '/posts/int:post_id/like', '/posts/int:post_id/unlike')
    return app

if __name__ == '__main__':

    app= create_app()
    app.run(debug=True)
