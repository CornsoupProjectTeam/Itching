import uuid
from flask import Blueprint, request, jsonify
from app import db
from app.models.chat_room_quotation import ChatRoomQuotation
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

quotation_bp = Blueprint('quotation', __name__)

@quotation_bp.route('/check', methods=['POST'])
def create_quotation():
    """폼 데이터를 받아 제출된 견적서 내용을 JSON으로 반환"""
    try:
        # UUID 생성: 폼에 quotation_id가 비어 있으면 생성
        quotation_id = request.form.get('quotation_id') or str(uuid.uuid4())
        
        data = {
            "client_requirements": request.form.get('client_requirements'),
            "quotation_id": quotation_id,  # UUID를 사용한 견적서 ID
            "quotation": float(request.form.get('quotation', 0)),  # 견적 금액을 가져옴
            "number_of_drafts": int(request.form.get('number_of_drafts')),
            "final_deadline": request.form.get('final_deadline'),
            "midterm_check": request.form.get('midterm_check'),
            "revision_count": int(request.form.get('revision_count')),
            "additional_revision_available": 'additional_revision_available' in request.form,
            "commercial_use_allowed": 'commercial_use_allowed' in request.form,
            "high_resolution_file_available": 'high_resolution_file_available' in request.form,
            "delivery_route": request.form.get('delivery_route')
        }

        # 제출된 데이터를 JSON 응답으로 반환
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@quotation_bp.route('/send', methods=['POST'])
def send_quotation():
    """폼 데이터를 받아서 데이터베이스에 저장하고 JSON 응답 반환"""
    try:
        # POST 요청의 폼 데이터 받기
        quotation_id = request.form.get('quotation_id') or str(uuid.uuid4())  # UUID로 고유한 ID 생성
        chat_room_id = request.form.get('chat_room_id')
        client_user_id = request.form.get('client_user_id')
        freelancer_user_id = request.form.get('freelancer_user_id')
        quotation_st = request.form.get('quotation_st', 'Submitted')  # 기본값 설정
        quotation = float(request.form.get('quotation', 0))
        number_of_drafts = int(request.form.get('number_of_drafts', 0))
        midterm_check = datetime.strptime(request.form.get('midterm_check', '2024-01-01'), '%Y-%m-%d')
        final_deadline = datetime.strptime(request.form.get('final_deadline', '2024-01-01'), '%Y-%m-%d')
        revision_count = int(request.form.get('revision_count', 0))
        additional_revision_available = 'additional_revision_available' in request.form
        commercial_use_allowed = 'commercial_use_allowed' in request.form
        high_resolution_file_available = 'high_resolution_file_available' in request.form
        delivery_route = request.form.get('delivery_route')

        # 새로운 견적서 객체 생성
        new_quotation = ChatRoomQuotation(
            quotation_id=quotation_id,  # 고유한 UUID 사용
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

        # DB에 저장
        db.session.add(new_quotation)
        db.session.commit()

        # 저장 완료 후 JSON 응답 반환
        return jsonify({"message": "Quotation saved successfully.", "quotation_id": quotation_id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
