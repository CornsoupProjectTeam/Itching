# app/repositories/chat_room_repository.py
from app.models.chat_room_master import ChatRoomMaster
from app import db

class ChatRoomRepository:
    def get_chat_rooms_by_user(self, user_id: str):
        """
        주어진 사용자 ID에 해당하는 채팅방 목록을 조회
        """
        try:
            return ChatRoomMaster.query.filter_by(user_id=user_id).all()
        except Exception as e:
            raise ValueError(f"Error retrieving chat rooms for user {user_id}: {e}")
    
    def get_chat_room_by_id(self, chat_room_id: str):
        """
        주어진 채팅방 ID에 해당하는 채팅방 정보를 조회
        """
        try:
            return ChatRoomMaster.query.filter_by(chat_room_id=chat_room_id).first()
        except Exception as e:
            raise ValueError(f"Error retrieving chat room {chat_room_id}: {e}")

    def update_trade_status(self, chat_room_id: str, new_status: str):
        """
        주어진 채팅방의 거래 상태를 업데이트
        """
        try:
            chat_room = self.get_chat_room_by_id(chat_room_id)
            if chat_room:
                chat_room.trade_st = new_status
                db.session.commit()
                return chat_room
            else:
                raise ValueError(f"Chat room {chat_room_id} not found.")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error updating trade status for chat room {chat_room_id}: {e}")

    def save_chat_room(self, chat_room: ChatRoomMaster):
        """
        새로운 채팅방을 데이터베이스에 저장
        """
        try:
            db.session.add(chat_room)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error saving chat room {chat_room.chat_room_id}: {e}")
    
    def delete_chat_room(self, chat_room_id: str):
        """
        주어진 채팅방 ID에 해당하는 채팅방을 삭제 (soft delete)
        """
        try:
            chat_room = self.get_chat_room_by_id(chat_room_id)
            if chat_room:
                chat_room.is_deleted = True
                db.session.commit()
            else:
                raise ValueError(f"Chat room {chat_room_id} not found.")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error deleting chat room {chat_room_id}: {e}")
