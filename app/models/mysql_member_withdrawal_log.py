# mysql_member_withdrawal_log.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MemberWithdrawalLog(db.Model):
    __tablename__ = 'MEMBER_WITHDRAWAL_LOG'

    user_id = db.Column(db.String(20), db.ForeignKey('LOGIN.user_id'), primary_key=True)
    reason = db.Column(db.String(255), nullable=True)
    withdrawal_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('LOGIN', backref='withdrawal_log')

    def __repr__(self):
        return self.user_id
