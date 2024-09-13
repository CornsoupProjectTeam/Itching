# mysql_member_withdrawal_log.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MemberWithdrawalLog(db.Model):
    __tablename__ = 'member_withdrawal_log'

    user_id = db.Column(db.String(20), db.ForeignKey('login.user_id'), primary_key=True)
    reason = db.Column(db.String(255), nullable=True)
    withdrawal_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('Login', backref='withdrawal_log')

    def __repr__(self):
        return self.user_id
