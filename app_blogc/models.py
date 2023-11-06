from datetime import datetime
from app_blogc import db


# association table to model many-to-many relationship
association_table = db.Table('association', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('followed_at', db.DateTime, default=datetime.utcnow)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password = db.Column(db.String(60), nullable=False)  # HASHED PASSWORD!
    created_date = db.Column(db.DateTime, default=datetime.utcnow)  
    posts = db.relationship('Post', back_populates='author', lazy=True, cascade="all, delete-orphan")
    groups = db.relationship('Group', secondary=association_table, backref='users')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic', cascade="all, delete-orphan")



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.relationship('User', back_populates='posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    favorited = db.relationship('Favorite', backref='post', lazy='dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='group', lazy=True)
