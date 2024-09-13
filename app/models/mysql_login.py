# mysql_login.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Login(db.Model):
    __tablename__ = 'LOGIN'

    user_id = db.Column(db.String(20), primary_key=True)
    provider_id = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return self.user_id
