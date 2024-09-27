from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ClientPost(db.Model):
    __tablename__ = 'CLIENT_POST'
    
    client_post_id = db.Column(db.String(50), primary_key=True)
    client_user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id'), nullable=False)
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code'), nullable=False)
    client_title = db.Column(db.String(200), nullable=False)
    client_payment_amount = db.Column(db.Integer, nullable=False)
    completion_deadline = db.Column(db.Date, nullable=False)
    posting_deadline = db.Column(db.Date, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('client_posts', lazy=True))
    field_keywords = db.relationship('FieldKeywords', backref=db.backref('client_posts', lazy=True))
