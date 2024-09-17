#견적서 : 이름 변결 필요

from flask import Blueprint, render_template, request, redirect, url_for
from app.models.chat_room import ChatRoom
from app.repositories.chat_room_repository import ChatRoomRepository

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            estimate = request.form.get('estimate')
            if not estimate:
                raise ValueError("Estimate 값이 입력되지 않았습니다.")
            
            data = {
                "estimate_id": request.form.get('estimate_id'),
                "participants": request.form.getlist('participants'),
                "estimate_status": request.form.get('estimate_status'),
                "requirements_mapping": [
                    {
                        "sequence": 1,
                        "requirement": request.form.get('requirement1')
                    },
                    {
                        "sequence": 2,
                        "requirement": request.form.get('requirement2')
                    }
                ],
                "estimate": int(estimate),
                "number_of_drafts": int(request.form.get('number_of_drafts')),
                "notification_dates": {
                    "midterm_check": request.form.get('midterm_check'),
                    "final_deadline": request.form.get('final_deadline')
                },
                "revision_count": int(request.form.get('revision_count')),
                "additional_revision_purchase_available": request.form.get('additional_revision_purchase_available') == 'on',
                "commercial_use_allowed": request.form.get('commercial_use_allowed') == 'on',
                "high_resolution_file_available": request.form.get('high_resolution_file_available') == 'on',
                "delivery_method": request.form.get('delivery_method'),
            }

            chat_room = ChatRoom(**data)
            ChatRoomRepository.insert_chat_room(chat_room.to_dict())

            # 데이터를 success.html로 전달
            return render_template('success.html', data=data)

        except ValueError as e:
            return f"Error: {str(e)}", 400

    return render_template('index.html')

