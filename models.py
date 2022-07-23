from enum import unique
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for users table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                    primary_key = True,
                    autoincrement = True)
    
    first_name = db.Column(db.String(50),
                            nullable = False)

    last_name = db.Column(db.String(50),
                            nullable = False)

    image_url = db.Column(db.String(300))

    def __repr__(self):
        return f'<First Name={self.first_name}, Last Name={self.last_name}>'

class Post(db.Model):
    """Models for posts table"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
    tagged_items = db.relationship('PostTag', backref='post')
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    def __repr__(self):
        return f'<Title: {self.title}, Content: {self.content}, Created: {self.created_at}, User: {self.user_id}>'

class Tag(db.Model):
    """Models for Tag table"""
    
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)

    tagged_items = db.relationship('PostTag', backref='tag')
    # posts = db.relationship('Post', secondary="posts_tags", backref='tags')

    def __repr__(self):
        return f'<Name: {self.name}>'

class PostTag(db.Model):
    """Model for PostTag table"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)  