# chat_room_quotation_routes.py
from flask import Blueprint, request, render_template
from datetime import datetime

quotation_bp = Blueprint('quotation', __name__)

@quotation_bp.route('/', methods=['GET'])
def quotation_form():
    """견적서 작성 페이지를 렌더링"""
    return render_template('chat_room_quotation.html')

@quotation_bp.route('/check', methods=['POST'])
def create_quotation():
    """폼 데이터를 받아 제출된 견적서 내용을 확인 페이지에 노출"""
    try:
        data = {
            "client_requirements": request.form.get('client_requirements'),
            "quotation": float(request.form.get('quotation')),
            "number_of_drafts": int(request.form.get('number_of_drafts')),
            "final_deadline": request.form.get('final_deadline'),
            "midterm_check": request.form.get('midterm_check'),
            "revision_count": int(request.form.get('revision_count')),
            "additional_revision_available": 'additional_revision_available' in request.form,
            "commercial_use_allowed": 'commercial_use_allowed' in request.form,
            "high_resolution_file_available": 'high_resolution_file_available' in request.form,
            "delivery_route": request.form.get('delivery_route')
        }

        # 제출된 데이터를 확인 페이지로 렌더링
        return render_template('chat_room_quotation_check.html', data=data)
    
    except Exception as e:
        return f"Error: {str(e)}", 500


