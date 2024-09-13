# mysql_postmanagement.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PostManagement(db.Model):
    __tablename__ = 'post_management'

    post_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('login.user_id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    reference_post_id = db.Column(db.String(50), nullable=True)
    project_title = db.Column(db.String(255), nullable=False)
    project_or_client_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Login', backref='posts')

    def __repr__(self):
        return self.post_id
