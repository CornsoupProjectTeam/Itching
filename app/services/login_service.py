#login_service.py

from app.domain.login_domain import User
from app.repositories.login_repository import LoginRepository
from app.models.login import Login
from flask import session
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import app, mail
from flask import session, url_for, jsonify
from app.models.user_information import UserInformation
from app.models.user_consent import UserConsent
from app.utils.encryption_util import EncryptionUtils
from authlib.integrations.flask_client import OAuth
from app.repositories.user_information_repository import UserInformationRepository
import secrets
import os

class LoginService:
    def __init__(self):
        self.user_repository = LoginRepository()
        self.serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        self.oauth = OAuth(app)
        self.google = self.oauth.register(
            name='google',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid profile email'}
        )

    def generate_token(self, email):
        """Generate a token for email verification."""
        return self.serializer.dumps(email, salt='email-confirm-salt')

    def sign_up(self, user_id, password, provider_id=None, email=None, personal_info_consent=None, terms_of_service_consent=None):
        if not User.validate_user_id(user_id):
            return "User ID must only contain lowercase letters and numbers.", False
    
        if not User.validate_password(password):
            return "Password must be at least 8 characters long and contain only lowercase letters and numbers.", False
        
        # 비밀번호를 암호화하여 저장
        hashed_password = EncryptionUtils.hash_password(password)

        new_user = Login(
            user_id=user_id,
            password=hashed_password,  # 암호화된 비밀번호 저장
            provider_id=provider_id,
            is_active=True
        )
        self.user_repository.save(new_user)

        try:
          # 사용자 정보 삽입
            user_info_repo = UserInformationRepository()
            user_info_repo.insert_new_user(
                user_id=user_id,
                email=email,
                profile_picture_path=None,
                nickname=None,
                business_area=None,
                preferred_fields=[],
                preferred_freelancers=[]
            )

            # 동의 정보 삽입
            if personal_info_consent is not None and terms_of_service_consent is not None:
                new_consent = UserConsent(
                    user_id=user_id,
                    personal_info_consent=personal_info_consent,
                    terms_of_service_consent=terms_of_service_consent
            )
            self.user_repository.save_user_consent(new_consent)

            return "User registered successfully", True

        except Exception as e:
            print(f"Error occurred: {e}")
            return "User registration failed.", False


        # # USER_INFORMATION에 사용자 정보 저장
        # user_info_repo = UserInformationRepository()
        # user_info_repo.insert_new_user(
        # user_id=user_id,
        # email=email,
        # profile_picture_path=None,
        # nickname=None,
        # business_area=None,
        # preferred_fields=[],
        # preferred_freelancers=[]
        # )

        # if personal_info_consent is not None and terms_of_service_consent is not None:
        #     new_consent = UserConsent(
        #         user_id=user_id,
        #         personal_info_consent=personal_info_consent,
        #         terms_of_service_consent=terms_of_service_consent
        #     )
        #     self.user_repository.save_user_consent(new_consent)

        # return "User registered successfully.", True
    
    def save_user_profile(self, user_id, email, nickname, business_area, profile_picture_path, preferred_freelancer_type_data):
        try:
            user_info_repo = UserInformationRepository()
            # UserProfile SQL에 저장
            user_profile_data = {
                "user_id": user_id,
                "email": email,
                "nickname": nickname,
                "business_area": business_area,
                "profile_picture_path": profile_picture_path,
                "preferred_freelancer_type_mapping": preferred_freelancer_type_data
        }
            user_info_repo.insert_new_user(user_profile_data)
            return True, "Profile saved successfully."
        except Exception as e:
            return False, str(e)
    
    def send_verification_email(self, email):
        # 이메일 값이 올바른지 디버깅 메시지 추가
        print(f"Email received for verification: {email}")

        if not email:
            raise ValueError("Email is missing")  # 추가된 예외 처리

        # 이메일 인증 링크 생성
        try: 
            token = self.generate_token(email)
            confirm_url = url_for('login_bp.verify_email', token=token, _external=True)

            # 디버깅 메시지 추가 (확인용)
            print(f"Generated token: {token}")
            print(f"Confirmation URL: {confirm_url}")

        except Exception as e:
            print(f"Error generating confirmation URL: {e}")
            raise ValueError("Verification link generation failed")  # 추가된 예외 처리

        # 필수 헤더 확인
        if not email or not confirm_url:
            raise ValueError("Email or verification link is missing")

        # 이메일 전송
        msg = Message('Email Verification', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = f'Please click the link to verify your email: {confirm_url}'
        mail.send(msg)
        return {"message": "Email sent for verification. Please check your email.", "success": True}, 200

    def verify_email_token(self, token):
        try:
            email = self.serializer.loads(token, salt='email-confirm-salt', max_age=3600)  # 1시간 유효
            user = self.user_repository.find_by_user_id(email)
            if user:
                user.is_active = True  # 이메일 인증 상태 갱신
                self.user_repository.update(user)
                return True
            else:
                return False
        
        except Exception as e:
            print(f"Email verification failed: {e}")
            return False

    def login(self, user_id, password):
        user = self.user_repository.find_by_user_id(user_id)
        if not user:
            return "User does not exist", False
        
        print(f"Stored password hash: {user.password}")
        print(f"Input password: {password}")

        # 입력한 비밀번호와 해시된 비밀번호를 비교
        if user.password and EncryptionUtils.check_password(password, user.password):
            session['user_id'] = user.user_id
            return "Login successful", True

        return "Invalid credentials", False


    def logout(self):
        session.pop('user_id', None)
        return "Logout successful", True

    def send_password_reset_link(self, email, user_id=None):
        """비밀번호 재설정 링크 전송"""

        # UserInformationRepository 인스턴스 생성
        user_info_repo = UserInformationRepository()

        if user_id:
            user = user_info_repo.get_user_info_by_user_id(user_id)
            if not user or user['user_info']['email'] != email: 
                return "User not found.", False

        token = self.generate_token(email)
        reset_url = url_for('login_bp.reset_password', token=token, _external=True)

        msg = Message('Password Reset Request', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = f"To reset your password, click the link: {reset_url}"
        mail.send(msg)
        return "Password reset link sent to your email.", True

    def reset_password(self, token, new_password):
        """비밀번호 재설정 처리 -> 비밀번호 까먹었을 때"""
        
        try:
            email = self.serializer.loads(token, salt='email-confirm-salt', max_age=3600)
            user = self.user_repository.find_by_user_id(email)
            if user:
                hashed_password = EncryptionUtils.hash_password(new_password)
                user.password = hashed_password
                self.user_repository.update(user)
                return "Password updated successfully.", True
            return "Invalid token or user not found.", False
        except Exception as e:
            print(f"Password reset failed: {e}")
            return "Password reset failed.", False


    def find_or_create_social_user(self, provider_id, provider_name, personal_info_consent=None, terms_of_service_consent=None):
        # 소셜 로그인인 경우 provider_id를 사용하여 조회
        if provider_name:
            user = self.user_repository.find_by_provider_id(provider_id)
        else:
            # 로컬 로그인인 경우 user_id를 provider_id로 사용하여 조회
            user = self.user_repository.find_by_user_id(provider_id)

        if not user:
            new_user = Login(
                USER_ID=provider_id,  # USER_ID를 provider_id로 사용 (소셜 및 로컬 모두 동일)
                PROVIDER_ID=provider_name,  # 소셜 로그인인 경우 provider_name 저장, 로컬 로그인인 경우 None
                IS_ACTIVE=True
            )
    
            if personal_info_consent is not None and terms_of_service_consent is not None:
                new_consent = UserConsent(
                    user_id=provider_id,
                    personal_info_consent=personal_info_consent,
                    terms_of_service_consent=terms_of_service_consent
                )
                self.user_repository.save_user_consent(new_consent)
            return new_user
        return user
    
    def check_user_id_exists(self, user_id):
        """아이디 중복 확인"""
        return self.user_repository.find_by_user_id(user_id) is not None

    def check_nickname_exists(self, nickname):
        """닉네임 중복 확인"""
        return self.user_repository.find_by_nickname(nickname) is not None

    def send_welcome_email(self, email):
        """회원가입 완료 후 환영 이메일 전송"""
        if not email:
            raise ValueError("Email is missing for sending welcome email")

        # 이메일 내용 작성
        subject = "Welcome to Our Service"
        body = "회원가입이 완료되었습니다. 서비스를 이용해주셔서 감사합니다."

        # 이메일 전송
        msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = body
        try:
            mail.send(msg)
            print(f"Welcome email sent to {email}")
        except Exception as e:
            print(f"Failed to send welcome email to {email}: {e}")

    def find_user_id_by_email(self, email):
        """이메일을 통해 사용자 ID를 찾고, 이메일로 전송"""
        user_info_repo = UserInformationRepository()
        
        user_profile = user_info_repo.get_user_by_email(email)

        if not user_profile['success']:
            return "User not found.", False
        
        user_id = user_profile['user_info'].user_id

        msg = Message('Your ID Information', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = f"Your ID is: {user_id}"
        mail.send(msg)
        return "User ID sent to your email.", True
    
    def google_oauth_signup(self):
        """Google OAuth 회원가입 시작"""
        redirect_uri = url_for('login_bp.google_signup_callback', _external=True)
        nonce = secrets.token_urlsafe(16)
        session['nonce'] = nonce
        return self.google.authorize_redirect(redirect_uri, nonce=nonce)

    def google_oauth_signup_callback(self):
        """Google OAuth 회원가입 콜백"""
        try:
            token = self.google.authorize_access_token()
            if not token:
                return "Failed to fetch token", False

            nonce = session.pop('nonce', None)
            if not nonce:
                return "Nonce not found in session", False

            user_info = self.google.parse_id_token(token, nonce=nonce)
            if not user_info:
                return "Failed to parse ID token", False

            user_id = user_info['sub']
            email = user_info.get('email')
            name = user_info.get('name')

            user = self.find_or_create_social_user(user_id, 'google')

            session['user_id'] = user.USER_ID
            return email, user_id, True
        except Exception as e:
            return str(e), False

    def google_oauth_login(self):
        """Google OAuth 로그인 시작"""
        redirect_uri = url_for('login_bp.google_callback', _external=True)
        nonce = secrets.token_urlsafe(16)
        session['nonce'] = nonce
        return self.google.authorize_redirect(redirect_uri, nonce=nonce)

    def google_oauth_login_callback(self):
        """Google OAuth 콜백 시작"""
        try:
            token = self.google.authorize_access_token()
            if not token:
                return "Failed to fetch token", False

            nonce = session.pop('nonce', None)
            if not nonce:
                return "Nonce not found in session", False

            user_info = self.google.parse_id_token(token, nonce=nonce)
            if not user_info:
                return "Failed to parse ID token", False

            provider_id = user_info['sub']
            email = user_info.get('email')

            user = self.find_or_create_social_user(provider_id, 'google')

            session['user_id'] = user.user_id
            # 반환 값을 딕셔너리로 변경
            return {"email": email, "provider_id": provider_id}, True
        except Exception as e:
            return str(e), False

    
    def change_password(self, user_id: str, current_password: str, new_password: str, confirm_new_password: str) -> dict:
        # 1. 현재 비밀번호 확인
        hashed_current_password = self.user_repository.get_password_by_user_id(user_id)
        if not hashed_current_password:
            return {'success': False, 'message': '소셜 로그인 계정은 비밀번호 변경이 불가능합니다.'}

        # 2. 기존 비밀번호와 일치하는지 확인
        if not EncryptionUtils.check_password(current_password, hashed_current_password):
            return {'success': False, 'message': '기존 비밀번호가 일치하지 않습니다.'}

        # 3. 새 비밀번호와 확인용 비밀번호가 일치하는지 확인
        if new_password != confirm_new_password:
            return {'success': False, 'message': '새 비밀번호와 비밀번호 확인이 일치하지 않습니다.'}

        # 4. 새 비밀번호 유효성 검사
        if not User.validate_password(new_password):
            return {'success': False, 'message': '새로운 비밀번호는 8자 이상 소문자 영어 알파벳(a-z)와 숫자(0-9)로만 이루어져야 합니다.'}
        
        # 5. 새 비밀번호 해시 처리
        hashed_new_password = EncryptionUtils.hash_password(new_password)

        # 6. 새 비밀번호 저장
        result = self.user_repository.save_new_password(user_id, hashed_new_password)
        if result['success']:
            return {'success': True, 'message': '비밀번호가 성공적으로 변경되었습니다.'}
        else:
            return {'success': False, 'message': '비밀번호 변경에 실패하였습니다.'}
