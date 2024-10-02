from app import db
from datetime import datetime

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
    
    # version_code와 sequence를 개별적으로 처리하는 관계 설정
    pretest_condition_version = db.relationship(
        'PretestCondition',
        foreign_keys=[version_code],
        backref=db.backref('scanner_requirements_version', lazy=True, cascade="all, delete-orphan")
    )

    pretest_condition_sequence = db.relationship(
        'PretestCondition',
        foreign_keys=[sequence],
        backref=db.backref('scanner_requirements_sequence', lazy=True, cascade="all, delete-orphan")
    )