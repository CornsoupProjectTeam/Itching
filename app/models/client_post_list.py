from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ClientPostList(db.Model):
    __tablename__ = 'CLIENT_POST_LIST'
    
    client_post_id = db.Column(db.String(50), db.ForeignKey('CLIENT_POST.client_post_id', ondelete='CASCADE'), primary_key=True) 
    client_user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False) 
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code', ondelete='CASCADE'), nullable=False) 
    client_title = db.Column(db.String(200))
    client_payment_amount = db.Column(db.Integer)
    desired_deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client_post = db.relationship('ClientPost', backref=db.backref('client_post_lists', uselist=False, cascade="all, delete-orphan"))
    user_information = db.relationship('UserInformation', backref=db.backref('client_post_lists', lazy=True, cascade="all, delete-orphan"))
    field_keywords = db.relationship('FieldKeywords', backref=db.backref('client_post_lists', lazy=True, cascade="all, delete-orphan"))
