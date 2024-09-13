# mysql_favorite_list.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FavoriteList(db.Model):
    __tablename__ = 'favorite_list'

    favorite_list_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('login.user_id'), nullable=False)
    author_id = db.Column(db.String(20), db.ForeignKey('login.user_id'), nullable=False)
    favorite_post_id = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('Login', foreign_keys=[user_id], backref='favorites')
    author = db.relationship('Login', foreign_keys=[author_id], backref='favorite_authors')

    def __repr__(self):
        return self.favorite_list_id
