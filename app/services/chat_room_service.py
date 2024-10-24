# app/services/chat_room_service.py
import uuid
import os
import mimetypes
import base64
from app.domain.chat_room_domain import ChatRoom, Message
from app.models.chat_room_master import ChatRoomMaster
from app.models.mongo_message import MongoMessage
from datetime import datetime
from app import db
from pymongo import MongoClient
from app.repositories.chat_room_repository import ChatRoomRepository
from app.models.mongo_message import MongoMessage
from flask import render_template


class ChatRoomService:
    def __init__(self, mongo_uri):
        self.mongo_message = MongoMessage(mongo_uri=mongo_uri, db_name="itching_mongodb", collection_name="Message")

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
    
class ChatService:
    def __init__(self):
        self.chat_room_repository = ChatRoomRepository()
        self.mongo_message = MongoMessage(os.getenv('MONGO_URI'), 'itching_mongodb')

    # 채팅방 페이지 렌더링
    def render_chat_page(self):
        return render_template('chat.html')

    # 채팅방 접속 처리
    def join_chat_room(self, username, other_user_id, chat_room_id, user_type):
        chat_room = self.chat_room_repository.get_chat_room_by_id(chat_room_id)

        if not chat_room:
            # 새로운 채팅방 생성
            chat_room = self.chat_room_repository.save_chat_room(
                chat_room_id=chat_room_id,
                user_id=username,
                other_user_id=other_user_id,
                user_type=user_type
            )
        return chat_room.to_dict()

    # 메시지 처리
    def handle_message(self, chat_room_id, username, message_content):
        # 채팅방 정보 가져오기
        chat_room = self.chat_room_repository.get_chat_room_by_id(chat_room_id)
        
        if not chat_room:
            print(f"Chat room {chat_room_id} not found for user {username}")
            return

        # 상대방 ID 가져오기
        other_user_id = chat_room.other_user_id
        print(f"Message from {username} to {other_user_id}: {message_content}")


        # 메시지를 MongoDB에 저장
        message_id = self.mongo_message.save_message(
            sender_user_id=username,
            receiver_user_id=other_user_id,
            message_content=message_content
        )
        
        print(f"Message saved with ID {message_id}")
        
        # 클라이언트에 전송할 메시지 형식 정의
        return {
            'message_id': message_id,
            'username': username,
            'message_content': message_content
        }

    # 파일 업로드 처리
    def handle_file_upload(self, file_data, filename, chat_room_id):
        file_path = os.path.join('uploads', filename)
        
        # 파일 저장
        with open(file_path, 'wb') as f:
            f.write(bytearray(file_data))
        
        # 파일 MIME 타입 확인
        mime_type, _ = mimetypes.guess_type(file_path)

        # 파일 처리 (이미지 또는 PDF)
        if mime_type == "application/pdf":
            file_html = f"""
            <div>
                <a href="/uploads/{filename}" target="_blank" download="{filename}" style="color: #0d6efd;">📄 {filename}</a>
            </div>
            """
        elif mime_type and mime_type.startswith('image/'):
            encoded_data = base64.b64encode(file_data).decode('utf-8')
            file_html = f"""
            <div>
                <img src="data:{mime_type};base64,{encoded_data}" alt="{filename}" style="max-width: 100%; height: auto;">
                <a href="/uploads/{filename}" download="{filename}">다운로드</a>
            </div>
            """
        else:
            file_html = f'<a href="/uploads/{filename}" download>{filename}</a>'
        
        # 파일 전송
        return {
            'file_html': file_html
        }