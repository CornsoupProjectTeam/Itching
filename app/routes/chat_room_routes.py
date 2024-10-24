# app/routes/chat_room_routes.py
from flask import Blueprint, jsonify, request, redirect, url_for
from flask_socketio import emit, join_room, leave_room
from app.domain.chat_room_domain import ChatRoom, Message
from app.models.chat_room_master import ChatRoomMaster
from app.services.chat_room_service import ChatRoomService, ChatService
from app.models.mongo_message import MongoMessage
import os
from dotenv import load_dotenv
from app import db
from datetime import datetime

# .env 파일에서 환경 변수 로드
load_dotenv()

# MongoDB URI 환경 변수에서 불러오기
mongo_uri = os.getenv('MONGO_URI')

# ChatRoomService 인스턴스 초기화
chat_room_service = ChatRoomService(mongo_uri=mongo_uri)

chat_room_bp = Blueprint('chat_room_bp', __name__)

chat_service = ChatService()


# 채팅방 목록 조회 (MySQL)
@chat_room_bp.route('/list', methods=['GET'])
def get_chat_rooms():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    chat_rooms = chat_room_service.get_chat_rooms(user_id)
    return jsonify(chat_rooms), 200

# 채팅방 생성 (MySQL)
@chat_room_bp.route('/chat_room', methods=['POST'])
def create_chat_room():
    data = request.get_json()
    user_id = data.get('user_id')
    other_user_id = data.get('other_user_id')

    new_chat_room = chat_room_service.create_chat_room(user_id, other_user_id)
    return jsonify(new_chat_room), 201

# 거래가 시작된 글로 이동 (MySQL)
@chat_room_bp.route('/trade/<chat_room_id>', methods=['GET'])
def move_to_trade_post(chat_room_id):
    post_id = chat_room_service.move_to_trade_post(chat_room_id)
    if not post_id:
        return jsonify({"error": "Chat room not found"}), 404

    return redirect(url_for('client_post_bp.get_post', post_id=post_id))

# 메시지 조회 (NoSQL)
@chat_room_bp.route('/chat_room/<chat_room_id>/messages', methods=['GET'])
def get_chat_room_messages(chat_room_id):
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    messages = chat_room_service.get_chat_room_messages(chat_room_id, user_id)
    if not messages:
        return jsonify({"message": "No messages found"}), 404

    return jsonify({"chat_room_id": chat_room_id, "user_id": user_id, "messages": messages}), 200

# 메시지 저장 (NoSQL)
@chat_room_bp.route('/chat_room/<chat_room_id>/messages', methods=['POST'])
def save_message(chat_room_id):
    data = request.get_json()
    sender_user_id = data.get('sender_user_id')
    receiver_user_id = data.get('receiver_user_id')
    message_content = data.get('message_content')

    message_id = chat_room_service.save_message(sender_user_id, receiver_user_id, message_content)
    return jsonify({"message_id": message_id}), 201

# 거래 취소 (MySQL)
@chat_room_bp.route('/cancel/<chat_room_id>', methods=['POST'])
def cancel_trade(chat_room_id):
    # 채팅방 ID를 기준으로 채팅방을 조회
    chat_room = ChatRoomMaster.query.filter_by(chat_room_id=chat_room_id).first()
    
    if not chat_room:
        return jsonify({"error": "Chat room not found"}), 404
    
    try:
        # 거래 상태를 'Canceled'로 업데이트
        chat_room.trade_st = 'Canceled'
        chat_room.updated_at = datetime.utcnow()  # 마지막 업데이트 시간 수정
        
        db.session.commit()  # 변경 사항 저장
        return jsonify({"message": "Trade canceled successfully"}), 200
    
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": str(e)}), 500


# 거래 완료 (MySQL)
@chat_room_bp.route('/complete/<chat_room_id>', methods=['POST'])
def complete_trade(chat_room_id):
    chat_room = chat_room_service.complete_trade(chat_room_id)
    if not chat_room:
        return jsonify({"error": "Chat room not found"}), 404
    return jsonify({"message": "Trade completed successfully"}), 200

# 견적서로 이동
@chat_room_bp.route('/quotation/<chat_room_id>', methods=['GET'])
def move_to_quotation(chat_room_id):
    chat_room = ChatRoomMaster.query.filter_by(chat_room_id=chat_room_id).first()
    
    if not chat_room:
        return jsonify({"error": "Chat room not found"}), 404
    
    # 견적서 페이지로 리다이렉트
    return redirect(url_for('quotation.get_quotation', chat_room_id=chat_room.chat_room_id))

# 스캐너로 이동
@chat_room_bp.route('/scanner/<chat_room_id>', methods=['GET'])
def move_to_scanner(chat_room_id):
    return redirect(url_for('scanner_bp.scan', chat_room_id=chat_room_id))
