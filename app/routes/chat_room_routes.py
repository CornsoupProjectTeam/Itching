# chat_room_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from ..models.mysql_chat_room_master import ChatRoomMaster, db
from app.models.mysql_chat_room_master import ChatRoomMaster
from ..models.mongodb_chat_room_management import ChatRoomManagement

chat_blueprint = Blueprint('chat', __name__, url_prefix='/chat')

# 채팅방 리스트 렌더링
@chat_blueprint.route('/list', methods=['GET'])
def chat_rooms():
    chat_rooms = ChatRoomMaster.query.all()  # MySQL에서 채팅방 목록 가져오기
    return render_template('chat_room_list.html', chat_rooms=chat_rooms)

# 특정 채팅방 입장
@chat_blueprint.route('/room/<chat_room_id>', methods=['GET', 'POST'])
def chat_room(chat_room_id):
    # MySQL에서 채팅방 정보 가져오기
    chat_room = ChatRoomMaster.query.filter_by(chat_room_id=chat_room_id).first()

    # MongoDB에서 채팅 메시지 가져오기
    chat_room_mongo = ChatRoomManagement.objects(chat_room_id=chat_room_id).first()

    if request.method == 'POST':
        message = request.form.get('message')
        sender_user_id = request.form.get('sender_user_id')  # 예: 로그인한 사용자의 ID
        if chat_room_mongo:
            chat_room_mongo.add_message(sender_user_id, message)  # 새 메시지 추가

    return render_template('chat_room.html', chat_room=chat_room, messages=chat_room_mongo.message_mapping if chat_room_mongo else [])

# 파일 전송 처리 (jpg, png 파일만 허용)
@chat_blueprint.route('/send_file', methods=['POST'])
def send_file():
    file = request.files['file']
    if file and file.filename.split('.')[-1] in ['jpg', 'png']:
        # 파일 저장 로직 추가 (예: 로컬 저장, 또는 클라우드 스토리지 업로드)
        return '파일이 성공적으로 전송되었습니다.'
    return 'jpg 또는 png 파일만 전송 가능합니다.'


