#app/modles/chat_room_quotation.py
from app import db
from datetime import datetime

class ChatRoomQuotation(db.Model):
    __tablename__ = 'CHAT_ROOM_QUOTATION'
    
    quotation_id = db.Column(db.String(50), primary_key=True)
    chat_room_id = db.Column(db.String(50), db.ForeignKey('CHAT_ROOM_MASTER.chat_room_id', ondelete='CASCADE'), nullable=False) 
    client_user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)  
    freelancer_user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)
    quotation_st = db.Column(db.Enum('Submitted', 'Accepted', 'Updated')) # 견적서 수정을 위해 update 추가
    quotation = db.Column(db.Numeric(10, 2))
    number_of_drafts = db.Column(db.Integer)
    midterm_check = db.Column(db.Date)
    final_deadline = db.Column(db.Date, nullable=False)
    revision_count = db.Column(db.Integer)
    additional_revision_purchase_available = db.Column(db.Boolean)
    commercial_use_allowed = db.Column(db.Boolean)
    high_resolution_file_available = db.Column(db.Boolean)
    delivery_route = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    chat_room_master = db.relationship('ChatRoomMaster', backref=db.backref('quotations', lazy=True, cascade="all, delete-orphan"))
    client_user = db.relationship('UserInformation', foreign_keys=[client_user_id], backref=db.backref('client_quotations', lazy=True, cascade="all, delete-orphan"))
    freelancer_user = db.relationship('UserInformation', foreign_keys=[freelancer_user_id], backref=db.backref('freelancer_quotations', lazy=True, cascade="all, delete-orphan"))
