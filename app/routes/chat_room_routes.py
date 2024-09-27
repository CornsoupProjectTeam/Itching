# app/routes/chat_room_routes.py
from flask import Blueprint
from app.services.chat_room_service import ChatRoomService
from app import socketio
from flask_socketio import emit, join_room
from flask import Flask, render_template


chat_room_blueprint = Blueprint('chat_room', __name__)
chat_room_service = ChatRoomService()

# 새로운 거래가 시작된 페이지로 이동하는 라우트
@chat_room_blueprint.route('/transaction-started')
def transaction_page():
    return render_template('transaction_started.html')

# 스캐너로 이동하는 라우트
@chat_room_blueprint.route('/scanner')
def scanner_page():
    return render_template('scanner.html')

# 견적서로 이동하는 라우트
@chat_room_blueprint.route('/quotation/')
def quotation_page():
    return render_template('quotation.html')


# 채팅방 접속
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'message': f'User {data["username"]} has entered the room.'}, to=room)

# 채팅 메시지 전송 (sender -> receiver)
@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['message']
    
    # 메시지 저장
    chat_room_service.send_message(room, sender_id, receiver_id, message)
    
    # 수신자에게 메시지 전송
    emit('message', {'sender_id': sender_id, 'message': message}, to=room)

# 수신된 메시지 가져오기
@socketio.on('get_received_messages')
def handle_get_received_messages(data):
    room = data['room']
    user_id = data['user_id']
    
    # 사용자가 수신한 메시지를 가져와서 클라이언트에 전송
    received_messages = chat_room_service.get_received_messages(room, user_id)
    emit('received_messages', {'messages': received_messages}, to=user_id)


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
    
