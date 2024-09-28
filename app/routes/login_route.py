#login_route.py

from flask import Blueprint, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from app.services.login_service import LoginService
from app.models.user_information import UserInformation
from app import app
from flask_mail import Message
from mongoengine.queryset.visitor import Q
from app import mail
import secrets
import os

# Blueprint 정의
login_bp = Blueprint('login_bp', __name__)
login_service = LoginService()
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id = os.getenv('GOOGLE_CLIENT_ID'),
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}
)

@login_bp.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    email = data.get('email')
    
    # 이메일이 없는 경우 예외 처리
    if not email:
        return jsonify({"message": "Email is required.", "success": False}), 400
    
    # 이메일 인증 링크 전송
    message, success = login_service.send_verification_email(email)
    return jsonify({"message": message, "success": success}), (200 if success else 400)


@login_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    # 이메일 토큰 검증 및 처리
    if login_service.verify_email_token(token):
        return redirect(url_for('login_bp.signup_info'))
    else:
        return jsonify({"message": "Invalid or expired token"}), 400

@login_bp.route('/signup/info', methods=['GET', 'POST'])
def signup_info():
    if request.method == 'GET':
        # GET 요청의 경우 사용자가 소셜 로그인 후 들어오는 화면
        email = request.args.get('email')
        user_id = request.args.get('user_id')
        return jsonify({"message": "Enter additional information", "email": email, "user_id": user_id}), 200
    
    # POST 요청의 경우 사용자가 로컬 로그인 후 들어오는 화면
    data = request.json
    user_id = data.get('USER_ID')
    password = data.get('PASSWORD')
    provider_id = data.get('PROVIDER_ID')
    email = data.get('EMAIL')  # 이미 인증된 email 사용
    nickname = data.get('NICKNAME')
    business_area = data.get('BUSINESS_AREA')
    profile_picture_path = data.get('PROFILE_PICTURE_PATH', None)
    personal_info_consent = data.get('PERSONAL_INFO_CONSENT')
    terms_of_service_consent = data.get('TERMS_OF_SERVICE_CONSENT')
    preferred_freelancer_type_data = data.get('PREFERRED_FREELANCER_TYPE_MAPPING', {})
    
    # MySQL에 Login 정보 저장 및 UserProfile 저장
    message, success = login_service.sign_up(user_id, password, provider_id, email, personal_info_consent=personal_info_consent, 
                                             terms_of_service_consent=terms_of_service_consent)
    
    if success:
        save_success, save_message = login_service.save_user_profile(
            user_id, email, nickname, business_area, profile_picture_path, preferred_freelancer_type_data
        )
        if save_success:
            # 회원가입 성공 후 환영 이메일 전송
            login_service.send_welcome_email(email)
            return jsonify({"message": "User profile saved successfully", "success": True}), 200
        else:
            return jsonify({"message": save_message, "success": False}), 400
    else:
        return jsonify({"message": message, "success": False}), 400

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('USER_ID')
    password = data.get('PASSWORD')
    
    message, success = login_service.login(user_id, password)
    return jsonify({"message": message, "success": success}), (200 if success else 400)

@login_bp.route('/logout', methods=['POST'])
def logout():
    message, success = login_service.logout()
    return jsonify({"message": message, "success": success}), (200 if success else 400)

@login_bp.route('/account/recovery', methods=['GET'])
def account_recovery():
    """아이디 및 비밀번호 찾기 페이지 렌더링"""
    return jsonify({"message": "Please enter your email to find ID or reset password."})

@login_bp.route('/account/recovery/find-id', methods=['POST'])
def find_id():
    """이메일을 통해 사용자 ID 찾기 이거 수정"""
    data = request.json
    email = data.get('EMAIL')

    if not email:
        return jsonify({"message": "Email is required.", "success": False}), 400
    
    user = UserInformation.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"message": "User not found with the provided email.", "success": False}), 404

    # 서비스 계층에서 사용자 ID 전송 처리
    message, success = login_service.send_user_id_by_email(email, user.user_id)
    
    return jsonify({"message": message, "success": success}), (200 if success else 400)

@login_bp.route('/account/recovery/reset-password', methods=['POST'])
def reset_password_request():
    data = request.json
    email = data.get('EMAIL') 
    user_id = data.get('USER_ID')

    if not email or not user_id:
        return jsonify({"message": "Email and User ID are required.", "success": False}), 400

    message, success = login_service.send_password_reset_link(email, user_id)
    return jsonify({"message": message, "success": success}), (200 if success else 400)

@login_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        return jsonify({"message": "Enter your new password."})

    # POST 요청 처리: 비밀번호 업데이트
    data = request.json
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"message": "New password is required.", "success": False}), 400

    # 서비스 계층에서 비밀번호 재설정 처리
    message, success = login_service.reset_password(token, new_password)
    return jsonify({"message": message, "success": success}), (200 if success else 400)

# Google OAuth 회원가입 시작
@login_bp.route('/signup/google', methods=['GET'], endpoint='google_signup')
def google_signup():
    return login_service.google_oauth_signup()

# Google OAuth 콜백
@login_bp.route('/signup/google/callback', methods=['GET'], endpoint='google_signup_callback')
def google_signup_callback():
    email, user_id, success = login_service.google_oauth_signup_callback()
    if success:
        return redirect(url_for('login_bp.signup_info', email=email, user_id=user_id))
    else:
        return jsonify({"error": email}), 400

# Google OAuth 로그인 시작
@login_bp.route('/login/google', methods=['GET'])
def google_login():
    return login_service.google_oauth_login()

# Google OAuth 로그인 콜백
@login_bp.route('/login/google/callback', methods=['GET'])
def google_callback():
    email, provider_id, success = login_service.google_oauth_login_callback()
    if success:
        return redirect(url_for('login_bp.signup_info', email=email, user_id=provider_id))
    else:
        return jsonify({"error": email}), 400

@app.route('/home')
def index():
    return "Welcome to the home page"