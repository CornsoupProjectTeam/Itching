from flask import Blueprint, jsonify, request, abort, render_template
from app.services.chat_room_list_service import ChatRoomService  # 경로 수정 
from app.repositories.chat_room_list_repository import ChatRoomRepository  # 경로 수정 
from app.models.mongodb_chat_room_management import ChatRoomManagement  # 경로 수정

# Flask의 Blueprint를 사용해 라우터 생성
chat_room_list_bp = Blueprint('chat_room_list', __name__)

# 의존성 주입: ChatRoomService 인스턴스 생성
def get_chat_room_service():
    db = None  # MongoDB 연결 객체가 필요한 경우 처리할 수 있습니다.
    chat_room_repository = ChatRoomRepository(db)
    return ChatRoomService(chat_room_repository)

# 사용자가 참여한 채팅방 목록을 HTML로 렌더링
@chat_room_list_bp.route("/chatroomlist", methods=["GET"])
def get_chat_room_list():
    user_id = request.args.get("user_id", "defalut_user_id")
    if not user_id:
        return abort(400, "user_id is required")
    
    service = get_chat_room_service()
    chat_rooms = service.get_filtered_and_sorted_chat_rooms_for_user(user_id)
    
    if not chat_rooms:
        return render_template("chat_room_list.html", chat_rooms=None)
    
    # 채팅방 데이터를 HTML로 넘겨줌
    chat_room_data = []
    for chat_room in chat_rooms:
        last_message_info = service.get_last_message_info_from_chat_room(chat_room)
        chat_room_data.append({
            "chat_room_id": chat_room.chat_room_id,
            "last_message": last_message_info["message"] if last_message_info else "No messages",
            "sender_id": last_message_info["sender_id"] if last_message_info else "Unknown",
            "updated_at": chat_room.updated_at
        })
    
    return render_template("chat_room_list.html", chat_rooms=chat_room_data)

# 특정 채팅방의 가장 최근 메시지를 JSON으로 반환
@chat_room_list_bp.route("/chatroomlist/<chat_room_id>/last_message", methods=["GET"])
def get_last_message_from_chat_room_list(chat_room_id):
    user_id = request.args.get("user_id")
    if not user_id:
        return abort(400, "user_id is required")

    service = get_chat_room_service()
    chat_rooms = service.get_all_chat_rooms_for_user(user_id)
    
    # 해당 채팅방이 사용자의 채팅방 목록에 있는지 확인
    chat_room = next((room for room in chat_rooms if room.chat_room_id == chat_room_id), None)
    if not chat_room:
        return abort(404, "Chat room not found")
    
    # 채팅방에서 가장 최근 메시지 정보 가져오기
    last_message_info = service.get_last_message_info_from_chat_room(chat_room)
    if not last_message_info:
        return abort(404, "No messages found in the chat room")
    
    return jsonify(last_message_info), 200

