#chat_room_quotation_repository.py
from app.models.chat_room_master import ChatRoomMaster
from app.models.chat_room_quotation import ChatRoomQuotation, db
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

class ChatRoomQuotationRepository:
    
    def get_by_id(self, quotation_id: str) -> Optional[ChatRoomQuotation]:
        """Quotation ID를 통해 견적서 조회"""
        try:
            return ChatRoomQuotation.query.filter_by(quotation_id=quotation_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving quotation: {e}")
            return None
    
    def save(self, quotation: ChatRoomQuotation) -> bool:
        """새로운 견적서 저장 또는 기존 견적서 업데이트"""
        try:
            db.session.add(quotation)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error saving quotation: {e}")
            return False

    def delete(self, quotation_id: str) -> bool:
        """견적서 삭제"""
        try:
            quotation = self.get_by_id(quotation_id)
            if quotation:
                db.session.delete(quotation)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting quotation: {e}")
            return False
