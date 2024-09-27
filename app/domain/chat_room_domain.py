# chat_room_domain.py
from datetime import datetime

class ChatRoom:
    def __init__(self, chat_room_id, quotation_id, freelancer_user_id, client_user_id, start_post_id, 
                 freelancer_trade_status, client_trade_status, created_at=None, updated_at=None, messages=None):
        self.chat_room_id = chat_room_id
        self.quotation_id = quotation_id
        self.freelancer_user_id = freelancer_user_id
        self.client_user_id = client_user_id
        self.start_post_id = start_post_id
        self.freelancer_trade_status = freelancer_trade_status
        self.client_trade_status = client_trade_status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.messages = messages or []  # 채팅 메시지 목록

    def add_message(self, sender_id, receiver_id, message_content):
        """채팅 메시지를 추가하고 발신자와 수신자를 지정"""
        message = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message_content': message_content,
            'created_at': datetime.now()
        }
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_messages_for_user(self, user_id):
        """특정 사용자가 수신한 메시지만 반환"""
        return [msg for msg in self.messages if msg['receiver_id'] == user_id]

