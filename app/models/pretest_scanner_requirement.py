from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PretestScannerRequirement(db.Model):
    __tablename__ = 'PRETEST_SCANNER_REQUIREMENT'
    
    scanner_requirement_id = db.Column(db.String(50), primary_key=True)
    pretest_scanner_id = db.Column(db.String(50), db.ForeignKey('PRETEST_SCANNER.pretest_scanner_id', ondelete='CASCADE')) 
    version_code = db.Column(db.String(20), db.ForeignKey('PRETEST_CONDITION.version_code', ondelete='CASCADE'))  
    sequence = db.Column(db.Integer, db.ForeignKey('PRETEST_CONDITION.sequence', ondelete='CASCADE')) 
    score = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    pretest_scanner = db.relationship('PretestScanner', backref=db.backref('requirements', lazy=True, cascade="all, delete-orphan"))
    pretest_condition = db.relationship('PretestCondition', backref=db.backref('scanner_requirements', lazy=True, cascade="all, delete-orphan"))
