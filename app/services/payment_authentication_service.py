#payment_authentication_service.py
from app.repositories.payment_repository import PaymentRepository
from app.repositories.login_repository import LoginRepository
import requests
import os
from flask import session, url_for

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

class AuthenticationService:

    @staticmethod
    def authenticate(chat_room_id, user_name, client_user_id, password):
            
        # 사용자 이름을 결제 테이블에 삽입
        PaymentRepository.insert_user_name(chat_room_id, user_name)

        # 로그인 정보 확인 (사용자 ID가 테이블에 존재하는지 확인)
        login_user = LoginRepository.find_by_user_id(client_user_id)
        
        # 사용자가 존재하지 않으면 에러 반환
        if not login_user:
            return False, "User ID verification failed."

        # 세션에서 사용자 ID를 확인하고 일치하는지 검증
        session_user_id = session.get('user_id')
        if session_user_id != client_user_id:
            return False, "Session user ID mismatch."
        

        if login_user.provider_id == 'google':
            # 구글 로그인 사용자의 경우 리프레시 토큰으로 액세스 토큰 갱신
            try:
                new_access_token = AuthenticationService.refresh_google_access_token(login_user.password)  # 여기서는 password 필드를 리프레시 토큰으로 사용한다고 가정
                return True, f"Google user re-authenticated successfully. New access token: {new_access_token}"
            except Exception as e:
                return False, str(e)
        else:
            # 비밀번호 검증
            if not AuthenticationDomain.verify_password(client_user_id, password):
                return False, "Password verification failed."

        return True, "User authenticated successfully."
    
    @staticmethod
    def get_google_authorization_url():
        
        google_provider_cfg = AuthenticationService.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = requests.Request('GET', authorization_endpoint, params={
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": url_for('authentication.google_callback', _external=True),
            "scope": "openid email profile",
            "response_type": "code"
        }).prepare().url

        return request_uri

    @staticmethod
    def get_google_tokens(code):
        
        google_provider_cfg = AuthenticationService.get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # 인증 코드를 사용하여 토큰 요청
        token_response = requests.post(
            token_endpoint,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": url_for('authentication.google_callback', _external=True),
                "grant_type": "authorization_code"
            }
        )

        if token_response.status_code == 200:
            return token_response.json()
        else:
            raise Exception("Failed to retrieve tokens from Google.")

    @staticmethod
    def refresh_google_access_token(refresh_token):
        
        #리프레시 토큰을 사용해 구글 액세스 토큰 갱신
        google_provider_cfg = AuthenticationService.get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        payload = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post(token_endpoint, data=payload)

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            raise Exception("Failed to refresh Google access token.")

    @staticmethod
    def google_login():
        
        return AuthenticationService.get_google_authorization_url()

    @staticmethod
    def google_callback(code):
        
        try:
            tokens = AuthenticationService.get_google_tokens(code)
            access_token = tokens["access_token"]
            refresh_token = tokens.get("refresh_token")

            # 리프레시 토큰을 사용해 새 액세스 토큰 발급
            new_access_token = AuthenticationService.refresh_google_access_token(refresh_token)

            return True, {"new_access_token": new_access_token, "refresh_token": refresh_token}
        except Exception as e:
            return False, str(e)
