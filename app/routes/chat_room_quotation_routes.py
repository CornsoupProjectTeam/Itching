#app/routes/chat_room_quotation_routes.py
import uuid
from flask import Blueprint, request, jsonify
from app import db
from app.models.chat_room_quotation import ChatRoomQuotation
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

# 블루프린트에 url_prefix 설정
quotation_bp = Blueprint('quotation', __name__, url_prefix='/chatroom/quotation')

#. 견적서 작성 및 견적서 확인
@quotation_bp.route('/check', methods=['POST'])
def create_quotation():
    """폼 데이터를 받아 제출된 견적서 내용을 JSON으로 반환"""
    try:
        # UUID 생성: 폼에 quotation_id가 비어 있으면 생성
        quotation_id = request.form.get('quotation_id') or str(uuid.uuid4())
        
        data = {
            "client_requirements": request.form.get('client_requirements'), # 클라이언트의 요구 사항
            "quotation_id": quotation_id,  # UUID를 사용한 견적서 ID
            "quotation": float(request.form.get('quotation', 0)),  # 견적 금액, 기본값은 0
            "number_of_drafts": int(request.form.get('number_of_drafts')), # 초안의 수
            "final_deadline": request.form.get('final_deadline'), # 최종 마감일
            "midterm_check": request.form.get('midterm_check'), # 중간 점검일
            "revision_count": int(request.form.get('revision_count')), # 수정 횟수
            "additional_revision_available": 'additional_revision_available' in request.form, # 추가 수정 가능 여부
            "commercial_use_allowed": 'commercial_use_allowed' in request.form, # 상업적 사용 허용 여부
            "high_resolution_file_available": 'high_resolution_file_available' in request.form, # 고해상도 파일 제공 여부
            "delivery_route": request.form.get('delivery_route') # 전달 방식
        }

        # 제출된 데이터를 JSON 응답으로 반환
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#. 견적서 전송하기
@quotation_bp.route('/send', methods=['POST'])
def send_quotation():
    """폼 데이터를 받아서 데이터베이스에 저장하고 JSON 응답 반환"""
    try:
        # POST 요청의 폼 데이터 받기
        quotation_id = request.form.get('quotation_id') or str(uuid.uuid4())  # UUID로 고유한 ID 생성
        chat_room_id = request.form.get('chat_room_id').strip() # 채팅방 ID
        client_user_id = request.form.get('client_user_id').strip()  # 클라이언트 사용자 ID
        freelancer_user_id = request.form.get('freelancer_user_id').strip()  # 프리랜서 사용자 ID
        quotation_st = request.form.get('quotation_st', 'Submitted').strip()   # 견적 상태
        quotation = float(request.form.get('quotation', 0)) # 견적 금액
        number_of_drafts = int(request.form.get('number_of_drafts', 0)) # 초안의 수
        
        # 날짜에서 공백 및 탭 제거 후 파싱
        midterm_check = datetime.strptime(request.form.get('midterm_check', '2024-01-01').strip(), '%Y-%m-%d') # 중간 점검일
        final_deadline = datetime.strptime(request.form.get('final_deadline', '2024-01-01').strip(), '%Y-%m-%d')  # 최종 기한
        
        revision_count = int(request.form.get('revision_count', 0))
        additional_revision_available = 'additional_revision_available' in request.form
        commercial_use_allowed = 'commercial_use_allowed' in request.form
        high_resolution_file_available = 'high_resolution_file_available' in request.form
        delivery_route = request.form.get('delivery_route').strip()  # 공백 제거

        # 새로운 견적서 객체 생성
        new_quotation = ChatRoomQuotation(
            quotation_id=quotation_id,  # 고유한 UUID 사용
            chat_room_id=chat_room_id,
            client_user_id=client_user_id,
            freelancer_user_id=freelancer_user_id,
            quotation_st=quotation_st,
            quotation=quotation,
            number_of_drafts=number_of_drafts, 
            midterm_check=midterm_check, # 중간 컨펌날 입력
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

#. 견적서 수정
@quotation_bp.route('/update/<quotation_id>', methods=['POST'])
def update_quotation(quotation_id):
    """견적서 수정"""
    try:
        # 기존 견적서 조회
        quotation = ChatRoomQuotation.query.filter_by(quotation_id=quotation_id).first()

        if not quotation:
            return jsonify({"error": "Quotation not found"}), 404

        # 수정할 폼 데이터 받기
        chat_room_id = request.form.get('chat_room_id').strip()
        client_user_id = request.form.get('client_user_id').strip()
        freelancer_user_id = request.form.get('freelancer_user_id').strip()
        
        # QUOTATION_ST 값 검증 (허용된 값만 사용)
        quotation_st = request.form.get('quotation_st', 'Submitted').strip()
        if quotation_st not in ['Submitted', 'Accepted', 'Updated']:
            return jsonify({"error": "Invalid QUOTATION_ST value. Must be 'Submitted', 'Accepted', or 'Updated'."}), 400

    # 기타 수정할 데이터 추출
        quotation_value = float(request.form.get('quotation', 0))
        number_of_drafts = int(request.form.get('number_of_drafts', 0))
        midterm_check = datetime.strptime(request.form.get('midterm_check', '2024-01-01').strip(), '%Y-%m-%d')
        final_deadline = datetime.strptime(request.form.get('final_deadline', '2024-01-01').strip(), '%Y-%m-%d')
        revision_count = int(request.form.get('revision_count', 0))
        additional_revision_available = 'additional_revision_available' in request.form
        commercial_use_allowed = 'commercial_use_allowed' in request.form
        high_resolution_file_available = 'high_resolution_file_available' in request.form
        delivery_route = request.form.get('delivery_route').strip()

        # 견적서 정보 업데이트
        quotation.chat_room_id = chat_room_id
        quotation.client_user_id = client_user_id
        quotation.freelancer_user_id = freelancer_user_id
        quotation.quotation_st = quotation_st
        quotation.quotation = quotation_value
        quotation.number_of_drafts = number_of_drafts
        quotation.midterm_check = midterm_check
        quotation.final_deadline = final_deadline
        quotation.revision_count = revision_count
        quotation.additional_revision_purchase_available = additional_revision_available
        quotation.commercial_use_allowed = commercial_use_allowed
        quotation.high_resolution_file_available = high_resolution_file_available
        quotation.delivery_route = delivery_route
        quotation.updated_at = datetime.utcnow()

        # DB에 저장
        db.session.commit()

        return jsonify({"message": "Quotation updated successfully.", "quotation_id": quotation_id}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#. 결제로 이동
@quotation_bp.route('/proceed_to_payment/<quotation_id>', methods=['POST'])
def proceed_to_payment(quotation_id):
    """견적서에 대해 결제로 이동 및 결제 성공/실패 처리"""
    try:
        # 견적서 조회
        quotation = ChatRoomQuotation.query.filter_by(quotation_id=quotation_id).first()

        if not quotation:
            return jsonify({"error": "Quotation not found"}), 404

        # 결제 페이지로 리디렉션 (유진언니가 생성한 payment와 연동되어야 함)
        payment_url = f"https://payment.example.com/pay?amount={quotation.quotation}&quotation_id={quotation_id}"

        #. 결제 URL 반환
        return jsonify({"message": "Proceed to payment", "payment_url": payment_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 결제 성공 처리
@quotation_bp.route('/payment_success/<quotation_id>', methods=['POST'])
def payment_success(quotation_id):
    """결제가 성공했을 때 처리"""
    try:
        # 결제가 성공했을 때, 견적서의 상태를 'Accepted'로 업데이트
        quotation = ChatRoomQuotation.query.filter_by(quotation_id=quotation_id).first()

        if not quotation:
            return jsonify({"error": "Quotation not found"}), 404

        # 견적서 상태를 'Accepted'로 업데이트
        quotation.quotation_st = 'Accepted'
        quotation.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({"message": "Payment successful", "quotation_id": quotation_id}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 결제 실패 처리
@quotation_bp.route('/payment_failure/<quotation_id>', methods=['POST'])
def payment_failure(quotation_id):
    """결제가 실패했을 때 처리"""
    try:
        # 결제가 실패했을 때 처리할 로직
        quotation = ChatRoomQuotation.query.filter_by(quotation_id=quotation_id).first()

        if not quotation:
            return jsonify({"error": "Quotation not found"}), 404

        # 결제 실패 상태를 저장할 필요가 없을 수도 있지만, 로그를 남기거나 상태를 'Submitted'로 유지
        return jsonify({"message": "Payment failed. Please try again.", "quotation_id": quotation_id}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 견적서 조회 엔드포인트
@quotation_bp.route('/<chat_room_id>', methods=['GET'])
def get_quotation(chat_room_id):
    # 채팅방 ID에 해당하는 견적서 정보를 반환하는 로직
    return jsonify({"message": f"Quotation for chat room {chat_room_id}"})
