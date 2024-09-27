from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Login(db.Model):
    __tablename__ = 'LOGIN'
    
    user_id = db.Column(db.String(20), primary_key=True)
    provider_id = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
