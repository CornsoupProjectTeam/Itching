#app/services/chat_room_quotation_service.py
from flask import Blueprint, request, render_template
from app import db
from app.models.chat_room_quotation import ChatRoomQuotation
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

quotation_bp = Blueprint('quotation', __name__)

@quotation_bp.route('/', methods=['GET'])
def quotation_form():
    """견적서 작성 페이지를 렌더링"""
    return render_template('chat_room_quotation.html')

@quotation_bp.route('/check', methods=['POST'])
def create_quotation():
    """폼 데이터를 받아서 데이터베이스에 저장"""
    try:
        # 디버깅을 위한 출력
        print("폼 데이터:", request.form)

        # POST 요청의 폼 데이터 받기
        quotation_id = request.form.get('quotation_id')
        chat_room_id = request.form.get('chat_room_id')
        client_user_id = request.form.get('client_user_id')
        freelancer_user_id = request.form.get('freelancer_user_id')
        quotation_st = request.form.get('quotation_st')
        quotation = float(request.form.get('quotation', 0))
        number_of_drafts = int(request.form.get('number_of_drafts', 0))
        midterm_check = datetime.strptime(request.form.get('midterm_check', '2024-01-01'), '%Y-%m-%d')
        final_deadline = datetime.strptime(request.form.get('final_deadline', '2024-01-01'), '%Y-%m-%d')
        revision_count = int(request.form.get('revision_count', 0))
        additional_revision_available = 'additional_revision_purchase_available' in request.form
        commercial_use_allowed = 'commercial_use_allowed' in request.form
        high_resolution_file_available = 'high_resolution_file_available' in request.form
        delivery_route = request.form.get('delivery_route')

        if not chat_room_id:
            return "chat_room_id is missing", 400

        new_quotation = ChatRoomQuotation(
            quotation_id=quotation_id,
            chat_room_id=chat_room_id,
            client_user_id=client_user_id,
            freelancer_user_id=freelancer_user_id,
            quotation_st=quotation_st,
            quotation=quotation,
            number_of_drafts=number_of_drafts,
            midterm_check=midterm_check,
            final_deadline=final_deadline,
            revision_count=revision_count,
            additional_revision_purchase_available=additional_revision_available,
            commercial_use_allowed=commercial_use_allowed,
            high_resolution_file_available=high_resolution_file_available,
            delivery_route=delivery_route,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(new_quotation)
        db.session.commit()

        return render_template('chat_room_quotation_check.html', data=new_quotation)

    except SQLAlchemyError as e:
        print(f"Error saving quotation: {e}")
        return "Error saving quotation", 500

    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}", 500

