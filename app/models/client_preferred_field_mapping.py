from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ClientPreferredFieldMapping(db.Model):
    __tablename__ = 'CLIENT_PREFERRED_FIELD_MAPPING'
    
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), primary_key=True)  
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code', ondelete='CASCADE'))
    
    user = db.relationship('UserInformation', backref=db.backref('client_preferred_fields', lazy=True, cascade="all, delete-orphan"))
    field_keyword = db.relationship('FieldKeywords', backref=db.backref('client_preferred_fields', lazy=True, cascade="all, delete-orphan"))