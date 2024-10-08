# app/services/chat_room_service.py
from app.models.chat_room_master import ChatRoomMaster
from app.models.mongo_message import MongoMessage
from app import db

class ChatRoomService:
    def __init__(self, mongo_uri):
        self.mongo_message = MongoMessage(mongo_uri=mongo_uri, db_name="itching_mongodb")

    # MySQL에서 채팅방 목록 조회
    def get_chat_rooms(self, user_id):
        chat_rooms = ChatRoomMaster.query.filter_by(user_id=user_id).all()
        return [chat_room.to_dict() for chat_room in chat_rooms]

    # MySQL에 채팅방 생성
    def create_chat_room(self, user_id, other_user_id):
        new_chat_room = ChatRoomMaster(
            user_id=user_id,
            other_user_id=other_user_id,
            trade_st='In progress'
        )
        db.session.add(new_chat_room)
        db.session.commit()
        return new_chat_room.to_dict()

    # 특정 거래 시작된 게시물로 이동
    def move_to_trade_post(self, chat_room_id):
        chat_room = ChatRoomMaster.query.filter_by(chat_room_id=chat_room_id).first()
        if not chat_room:
            return None
        return chat_room.start_post_id

    # NoSQL에서 메시지 조회
    def get_chat_room_messages(self, chat_room_id, user_id):
        messages = self.mongo_message.get_messages(chat_room_id, user_id)
        return messages

    # 메시지 저장 (NoSQL)
    def save_message(self, sender_user_id, receiver_user_id, message_content):
        return self.mongo_message.save_message(sender_user_id, receiver_user_id, message_content)

    # 거래 취소 (MySQL)
    def cancel_trade(self, chat_room_id):
        chat_room = ChatRoomMaster.query.filter_by(chat_room_id=chat_room_id).first()
        if not chat_room:
            return None
        chat_room.trade_st = 'Canceled'
        db.session.commit()
        return chat_room

    # 거래 완료 (MySQL)
    def complete_trade(self, chat_room_id):
        chat_room = ChatRoomMaster.query.filter_by(chat_room_id=chat_room_id).first()
        if not chat_room:
            return None
        chat_room.trade_st = 'Completed'
        db.session.commit()
        return chat_room
