# chat_room_list_routes.py
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.services.chat_room_list_service import ChatRoomService
import os

# Flask의 Blueprint를 사용해 라우터 생성
chat_room_list_bp = Blueprint('chat_room_list', __name__)

# 의존성 주입: ChatRoomService 인스턴스 생성
def get_chat_room_service():
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://cornsoup:Chobob311^^@210.110.103.135:27017/itching_mongodb?authSource=admin')
    return ChatRoomService(mongo_uri)

# 채팅방 목록을 HTML로 렌더링
@chat_room_list_bp.route("/", methods=["GET"])
def get_chat_room_list():
    user_id = request.args.get("user_id", "freelancer01")  # 기본값을 freelancer01로 설정
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    service = get_chat_room_service()
    chat_rooms = service.get_chat_rooms_for_user(user_id)

    if not chat_rooms:
        return render_template("chat_room_list.html", chat_rooms=None)

    # 채팅방 데이터를 HTML로 넘겨줌
    chat_room_data = []
    for chat_room in chat_rooms:
        last_message_info = chat_room.get("message_mapping", [])[-1] if chat_room.get("message_mapping") else None
        chat_room_data.append({
            "chat_room_id": chat_room["chat_room_id"],
            "client_user_id": chat_room["participants_mapping"]["client_user_id"],
            "last_message": last_message_info["message_content"] if last_message_info else "No messages",
            "sender_id": last_message_info["sender_user_id"] if last_message_info else "Unknown",
            "updated_at": chat_room["updated_at"]
        })

    return render_template("chat_room_list.html", chat_rooms=chat_room_data)

# 특정 채팅방으로 이동하는 라우트 추가
@chat_room_list_bp.route("/chat_room/<chat_room_id>", methods=["GET"])
def chat_room(chat_room_id):
    service = get_chat_room_service()
    
    # 채팅방 정보를 MongoDB에서 가져오기
    chat_room = service.get_chat_room_by_id(chat_room_id)

    if not chat_room:
        return jsonify({"error": "Chat room not found"}), 404

    return render_template("chat_room.html", chat_room=chat_room)
