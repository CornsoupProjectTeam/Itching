from app import db
from datetime import datetime

class PretestScanner(db.Model):
    __tablename__ = 'PRETEST_SCANNER'
    
    pretest_scanner_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('pretest_scanners', lazy=True, cascade="all, delete-orphan"))
