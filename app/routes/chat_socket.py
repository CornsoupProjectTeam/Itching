# app/routes/chat_socket.py
from flask_socketio import emit, join_room, send
from flask import request
from app.services.chat_room_service import ChatRoomService
from app.models.chat_room_master import ChatRoomMaster
from app.models.mongo_message import MongoMessage  # MongoMessage 추가
from app import socketio, db
from datetime import datetime

chat_room_service = ChatRoomService()
mongo_message = MongoMessage(mongo_uri='mongodb://cornsoup:Chobob311^^@210.110.103.135:27017/itching_mongodb?authSource=admin', db_name='itching_mongodb')


# 사용자 세션 ID를 저장할 딕셔너리
users = {}

# 클라이언트가 채팅방에 참여
@socketio.on('join')
def on_join(data):
    user_id = data['user_id']

    # DB에서 사용자의 채팅방 정보 조회
    chat_room = ChatRoomMaster.query.filter_by(user_id=user_id, is_deleted=False).first()

    if not chat_room:
        emit('error', {'message': 'Chat room not found'})
        return

    chat_room_id = chat_room.chat_room_id
    users[(chat_room_id, user_id)] = request.sid  # 채팅방 ID와 사용자 ID로 세션 저장
    print(f"User {user_id} has been assigned SID {request.sid} in room {chat_room_id}")

    join_room(chat_room_id)
    emit('message', {'message': f'{user_id} has entered the room.'}, room=chat_room_id)

@socketio.on('connect')
def handle_connect():
    print('Someone connected')
    emit('message', {'message': 'A user has joined'}, broadcast=True)

# 클라이언트로부터 메시지 전송
@socketio.on('send_message')
def handle_message(data):
    user_id = data['user_id']
    message_content = data['message']

    # 로그 출력
    print(f"Received message from: {user_id}, Message: {message_content}")

    # DB에서 사용자의 채팅방 정보 조회
    chat_room = ChatRoomMaster.query.filter_by(user_id=user_id, is_deleted=False).first()

    if not chat_room:
        emit('error', {'message': 'Chat room not found'})
        return

    chat_room_id = chat_room.chat_room_id

    # 서버가 클라이언트로 메시지 전송 (채팅방에만 브로드캐스트)
    emit('message', {'username': user_id, 'message': message_content}, room=chat_room_id)
    print('Message broadcasted to all clients in the room.')

    # 보낸 사용자에게도 메시지를 전송
    emit('message', {'username': user_id, 'message': message_content}, room=request.sid)

    # MongoDB에 메시지 저장
    mongo_message.save_message(
        sender_user_id=user_id, 
        receiver_user_id=chat_room.other_user_id, 
        message_content=message_content
    )

# 파일 업로드 처리 (소켓)
@socketio.on('file_upload')
def handle_file_upload(data):
    file_data = data['file']
    filename = data['filename']
    user_id = data['user_id']

    # DB에서 사용자의 채팅방 정보 조회
    chat_room = ChatRoomMaster.query.filter_by(user_id=user_id, is_deleted=False).first()

    if not chat_room:
        emit('error', {'message': 'Chat room not found'})
        return

    # 파일 저장 (ChatRoomService 사용)
    file_url = chat_room_service.handle_file_upload(file_data, filename, chat_room.chat_room_id)

    # 상대방 세션 ID 가져오기
    other_user_id = chat_room.other_user_id
    receiver_sid = users.get((chat_room.chat_room_id, other_user_id))

    if receiver_sid:
        emit('file_received', {'username': user_id, 'file_url': file_url}, room=receiver_sid)
    else:
        emit('error', {'message': 'The other user is not connected.'})

    emit('file_received', {'username': user_id, 'file_url': file_url}, room=request.sid)

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    for (room_id, user_id), value in list(users.items()):
        if value == sid:
            del users[(room_id, user_id)]
            print(f"User {user_id} has disconnected from room {room_id}")
            break
