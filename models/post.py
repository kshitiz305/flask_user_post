from ext import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('User', secondary='post_likes', backref=db.backref('liked_posts', lazy=True))

    def __repr__(self):
        return f"Post(id={self.id}, title='{self.title}')"


post_likes = db.Table('post_likes',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))

