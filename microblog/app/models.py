from datetime import datetime
from app import db, login
from flask_login import UserMixin # UserMixin, class that includes generic implementations of methods needed for Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5 # User avatar generator

# When adding new columns to schema, run these commands after:
# 1. flask db migrate -m "<Add relevant message here>"
# 2. flask db upgrade

# Association Tables:
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# Database Tables:
class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    followed = db.relationship('User', 
        secondary=followers,    # configures the association table that is used
        primaryjoin=(followers.c.follower_id == id),    # indicates the condition that links this to association table
        secondaryjoin=(followers.c.followed_id == id),  # indicates the condition that links other to association table
        backref=db.backref('followers', lazy='dynamic'),    # defines how the relationship will be accessed from this
        lazy='dynamic')

    def followed_posts(self):
        # join: create a temporary table that combines data from posts and follower tables
        # filter: only keep entires that have this user as a follower
        followed = Post.query \
            .join(followers, (followers.c.followed_id == Post.user_id)) \
            .filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)

        return followed.union(own).order_by(Post.timestamp.desc()) 


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Decorators/Loaders
# Helps Flask-Login to load user from database
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

