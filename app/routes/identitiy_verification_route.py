#identity_verification_route.py

from flask import Blueprint, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from app.services.identity_verification_service import IdentityVerificationService
from app import app
from app import mail
import secrets
import os

# Blueprint 정의
identity_verification_bp = Blueprint('identity_verification_bp', __name__)
identity_verification = IdentityVerificationService()
oauth = OAuth(app)

# SMS 본인 인증 서비스 인스턴스 생성
verification_service = IdentityVerificationService()

@identity_verification_bp.route('/freelancer/{user_id}/register/send_verification_code', methods=['POST'])
def send_verification_code():
    try:
        phone_number = request.json.get('phone_number')
        if not phone_number:
            return jsonify({"error": "전화번호가 제공되지 않았습니다."}), 400
        
        # 전화번호로 인증 코드 전송
        verification_service.send_verification_code(phone_number)
        return jsonify({"message": "인증 코드가 전송되었습니다."}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "SMS 전송에 실패했습니다."}), 500

@identity_verification_bp.route('/freelancer/{user_id}/register/verify_code', methods=['POST'])
def verify_code():
    try:
        user_id = request.json.get('user_id')
        phone_number = request.json.get('phone_number')
        input_code = request.json.get('verification_code')

        if not (user_id and phone_number and input_code):
            return jsonify({"error": "필수 정보가 제공되지 않았습니다."}), 400

        # 인증 코드 검증
        if verification_service.verify_code(user_id, phone_number, input_code):
            return jsonify({"message": "본인 인증이 완료되었습니다."}), 200
        else:
            return jsonify({"error": "인증 코드가 유효하지 않거나 만료되었습니다."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
