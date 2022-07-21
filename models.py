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

    def __repr__(self):
        return f'<Title: {self.title}, Content: {self.content}, Created: {self.created_at}, User: {self.user_id}>'
        