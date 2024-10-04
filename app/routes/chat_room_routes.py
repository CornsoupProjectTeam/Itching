# #chat_room_routes.py
# from flask import Blueprint, render_template, jsonify, request
# from flask_socketio import emit, join_room
# from app.services.chat_room_service import ChatRoomService
# from app import socketio, db  # db는 SQLAlchemy 인스턴스
# import os

# # Flask의 Blueprint를 사용해 라우터 생성
# chat_room_bp = Blueprint('chat_room', __name__)  # chat_room_blueprint에서 chat_room_bp로 변경

# # 의존성 주입: ChatRoomService 인스턴스 생성
# mongo_uri = os.getenv('MONGO_URI', 'mongodb://cornsoup:Chobob311^^@210.110.103.135:27017/itching_mongodb?authSource=admin')
# chat_room_service = ChatRoomService(mongo_uri=mongo_uri, db_session=db.session)  # db.session 전달

# # 새로운 거래가 시작된 페이지로 이동하는 라우트
# @chat_room_bp.route('/transaction-started')
# def transaction_page():
#     return render_template('transaction_started.html')

# # 스캐너로 이동하는 라우트
# @chat_room_bp.route('/scanner')
# def scanner_page():
#     return render_template('scanner.html')

# # 견적서로 이동하는 라우트
# @chat_room_bp.route('/quotation/')
# def quotation_page():
#     return render_template('chat_room_quotation.html')


# # 채팅방 접속
# @socketio.on('join')
# def handle_join(data):
#     room = data['room']
#     join_room(room)
#     emit('message', {'message': f'User {data["username"]} has entered the room.'}, to=room)

# # 채팅 메시지 전송 (sender -> receiver)
# @socketio.on('send_message')
# def handle_send_message(data):
#     room = data['room']
#     sender_id = data['sender_id']
#     receiver_id = data['receiver_id']
#     message = data['message']
    
#     # 메시지 저장
#     chat_room_service.send_message(room, sender_id, receiver_id, message)
    
#     # 수신자에게 메시지 전송
#     emit('message', {'sender_id': sender_id, 'message': message}, to=room)

# # 수신된 메시지 가져오기
# @socketio.on('get_received_messages')
# def handle_get_received_messages(data):
#     room = data['room']
#     user_id = data['user_id']
    
#     # 사용자가 수신한 메시지를 가져와서 클라이언트에 전송
#     received_messages = chat_room_service.get_received_messages(room, user_id)
#     emit('received_messages', {'messages': received_messages}, to=user_id)
    
# # 채팅방 목록을 HTML로 렌더링
# @chat_room_bp.route("/", methods=["GET"])
# def get_chat_room_list():
#     user_id = request.args.get("user_id", "freelancer01")  # 기본값을 freelancer01로 설정
#     if not user_id:
#         return jsonify({"error": "user_id is required"}), 400

#     chat_room_data = chat_room_service.get_chat_room_data(user_id)  # 서비스 계층에서 가공된 데이터를 받음

#     if not chat_room_data:
#         return render_template("chat_room_list.html", chat_rooms=None)

#     return render_template("chat_room_list.html", chat_rooms=chat_room_data)

# # 특정 채팅방으로 이동하는 라우트 추가
# @chat_room_bp.route("/chat_room/<chat_room_id>", methods=["GET"])
# def chat_room(chat_room_id):
#     # 채팅방 정보를 MongoDB에서 가져오기
#     chat_room = chat_room_service.get_chat_room_by_id(chat_room_id)

#     if not chat_room:
#         return jsonify({"error": "Chat room not found"}), 404

#     return render_template("chat_room.html", chat_room=chat_room)


# 거래 관련 라우트
# @chat_room_blueprint.route('/chat/start/<int:chat_room_id>')
# def start_transaction(chat_room_id):
#     chat_room_service.start_transaction(chat_room_id)
#     return redirect(url_for('chat_room.transaction_page', message="거래가 시작되었습니다."))

# @chat_room_blueprint.route('/chat/cancel/<int:chat_room_id>/<int:user_id>')
# def cancel_transaction(chat_room_id, user_id):
#     chat_room_service.cancel_transaction(chat_room_id, user_id)
#     return redirect(url_for('chat_room.transaction_page', message="거래가 취소되었습니다."))

# @chat_room_blueprint.route('/chat/complete/<int:chat_room_id>/<int:user_id>')
# def complete_transaction(chat_room_id, user_id):
#     chat_room_service.complete_transaction(chat_room_id, user_id)
#     return redirect(url_for('chat_room.transaction_page', message="거래가 완료되었습니다."))

#@chat_room_blueprint.route('/transaction')
#def transaction_page():
    #message = request.args.get('message', '')
    #return render_template('transaction.html', message=message)
    
    
from typing import List, Dict
from app.repositories.chat_room_repository import ChatRoomRepository
from app.models.mongodb_message_mapping import MessageMapping # MongoDB 메시지 모델
from flask import Blueprint, render_template, jsonify, request
from flask_socketio import emit, join_room
from app.services.chat_room_service import ChatRoomService
from app import socketio, db  # db는 SQLAlchemy 인스턴스
import os

# Flask의 Blueprint를 사용해 라우터 생성
chat_room_bp = Blueprint('chat_room', __name__)  # chat_room_blueprint에서 chat_room_bp로 변경

class ChatRoomService:
    def __init__(self, db_session):
        self.chat_room_repository = ChatRoomRepository(db_session)

    def get_chat_rooms_for_user(self, freelancer_user_id: str) -> List[Dict]:
        # MySQL에서 채팅방 데이터 가져오기
        chat_rooms = self.chat_room_repository.get_chat_rooms_by_user_id(freelancer_user_id)
        return chat_rooms

    def get_chat_room_data(self, freelancer_user_id: str) -> List[Dict]:
        chat_rooms = self.get_chat_rooms_for_user(freelancer_user_id)
        
        chat_room_data = []
        for chat_room in chat_rooms:
            last_message_info = self.chat_room_repository.get_most_recent_message(chat_room.chat_room_id, freelancer_user_id)
            chat_room_data.append({
                "chat_room_id": chat_room.chat_room_id,
                "client_user_id": chat_room.client_user_id,
                "last_message": last_message_info.message_content if last_message_info else "No messages",
                "sender_id": last_message_info.sender_user_id if last_message_info else "Unknown",
                "updated_at": chat_room.updated_at
            })

        return chat_room_data

    def get_chat_room_by_id(self, chat_room_id: str) -> Dict:
        # MySQL에서 채팅방 정보 가져오기
        chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        return chat_room

    def send_message(self, chat_room_id: str, sender_id: str, receiver_id: str, message: str):
        chat_room = self.chat_room_repository.find_by_id(chat_room_id)
        
        if chat_room:
            # 메시지를 MongoDB에 저장
            self.chat_room_repository.add_message(chat_room_id, sender_id, receiver_id, message)

    def get_received_messages(self, chat_room_id: str, user_id: str) -> List[Dict]:
        # MongoDB에서 받은 메시지 가져오기
        return self.chat_room_repository.get_chat_room_messages(chat_room_id)

    def get_most_recent_message(self, chat_room_id: str, user_id: str) -> Dict:
        # MongoDB에서 가장 최근 메시지 가져오기
        return self.chat_room_repository.get_most_recent_message(chat_room_id, user_id)

from flask import Blueprint, jsonify, request

chat_room_bp = Blueprint('chat_room', __name__)

@chat_room_bp.route('/message', methods=['POST'])
def send_message():
    from app import socketio  # 임포트 지연
    data = request.get_json()
    socketio.emit('message', data)
    return jsonify({'status': 'Message sent!'})


    
