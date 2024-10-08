# app/sockets/chat_socket.py
from flask_socketio import emit, join_room, leave_room
from app.services.chat_room_service import ChatService
from app import socketio

chat_service = ChatService(mongo_uri='your_mongo_uri', db_name='your_db_name')

@socketio.on('join')
def on_join(data):
    user_id = data['user_id']
    chat_room_id = data['chat_room_id']
    join_room(chat_room_id)
    emit('status', {'msg': f'{user_id} has entered the room.'}, room=chat_room_id)

@socketio.on('message')
def handle_message(data):
    chat_room_id = data['chat_room_id']
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message_content = data['message']

    # 메시지를 MongoDB에 저장
    chat_service.send_message(sender_id, receiver_id, message_content)
    emit('message', {'sender_id': sender_id, 'message': message_content}, room=chat_room_id)

@socketio.on('image')
def handle_image(data):
    chat_room_id = data['chat_room_id']
    sender_id = data['sender_id']
    image_data = data['image']

    # 이미지 처리를 위한 서비스 로직
    chat_service.save_image(sender_id, chat_room_id, image_data)
    emit('image', {'sender_id': sender_id, 'image': image_data}, room=chat_room_id)

@socketio.on('leave')
def on_leave(data):
    user_id = data['user_id']
    chat_room_id = data['chat_room_id']
    leave_room(chat_room_id)
    emit('status', {'msg': f'{user_id} has left the room.'}, room=chat_room_id)
