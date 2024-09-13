# mysql_client_post_list.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ClientPostList(db.Model):
    __tablename__ = 'client_post_list'

    client_post_id = db.Column(db.String(50), primary_key=True)
    client_user_id = db.Column(db.String(20), db.ForeignKey('login.user_id'), nullable=False)
    client_title = db.Column(db.String(200), nullable=True)
    client_payment_amount = db.Column(db.Integer, nullable=True)
    desired_deadline = db.Column(db.Date, nullable=True)
    final_deadline = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = db.relationship('Login', backref='client_posts')

    def __repr__(self):
        return f'<ClientPostList {self.client_post_id}>'
