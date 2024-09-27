# service/identity_verification_service.py

import requests
import time
import hashlib
import hmac
import base64
from app.repositories.identity_verification_repository import IdentityVerificationRepository
from app.domain.identity_verification_domain import IdentityVerificationDomain
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
import os


class IdentityVerificationService:
    def __init__(self):
        self.repository = IdentityVerificationRepository()
        # 네이버 클라우드 플랫폼 SMS API 설정
        self.sms_api_url = "https://sens.apigw.ntruss.com/sms/v2/services/{service_id}/messages"
        self.access_key = os.getenv("NAVER_ACCESS_KEY")  # 네이버 클라우드 액세스 키
        self.secret_key = os.getenv("NAVER_SECRET_KEY")  # 네이버 클라우드 시크릿 키
        self.service_id = os.getenv("NAVER_SERVICE_ID")  # 네이버 클라우드 서비스 ID
        self.sender_number = os.getenv("NAVER_SENDER_NUMBER")  # 발신자 전화번호

    def send_verification_code(self, phone_number):
        # 랜덤 6자리 인증 코드 생성
        verification_code = f"{random.randint(100000, 999999)}"
        expiration_time = datetime.utcnow() + timedelta(minutes=5)  # 인증 코드 5분 후 만료

        # 도메인 객체 생성 및 전화번호 유효성 검사
        domain = IdentityVerificationDomain(phone_number, verification_code, expiration_time)
        if not domain.is_valid_phone_number():
            raise ValueError("잘못된 전화번호 형식입니다")

        # SMS API 요청 보내기
        sms_response = self._send_sms(phone_number, verification_code)
        if sms_response.status_code != 202:
            raise Exception("SMS 전송 실패")

        # 레포지토리에 저장 (DB)
        self.repository.save_verification(phone_number, verification_code, expiration_time)

    """메서드 명을 소문자로 시작했으면 좋겠는데.."""
    def _make_signature(self, timestamp):
        # 네이버 클라우드 SMS API 서명을 생성하는 함수
        secret_key = bytes(self.secret_key, 'UTF-8')
        method = "POST"
        uri = f"/sms/v2/services/{self.service_id}/messages"
        message = method + " " + uri + "\n" + timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signing_key = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signing_key

    def _send_sms(self, phone_number, verification_code):
        # SMS API를 통해 인증 코드를 사용자에게 전송
        timestamp = str(int(time.time() * 1000))
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": self._make_signature(timestamp),
        }

        body = {
            "type": "SMS",
            "from": self.sender_number,
            "content": f"인증번호 [{verification_code}]를 입력해 주세요.",
            "messages": [{"to": phone_number}],
        }

        url = self.sms_api_url.format(service_id=self.service_id)
        response = requests.post(url, json=body, headers=headers)
        return response

    def verify_code(self, user_id, phone_number, input_code):
        # 저장소에서 저장된 인증 정보 가져오기
        verification_data = self.repository.get_verification_by_phone(phone_number)

        if not verification_data:
            raise ValueError("인증 데이터를 찾을 수 없습니다")

        # 도메인 객체를 생성하여 코드 검증
        domain = IdentityVerificationDomain(
            phone_number=verification_data.phone_number,
            verification_code=verification_data.verification_code,
            expiration_time=verification_data.expiration_time
        )

        if domain.is_verification_code_valid(input_code):
            # 레포지토리에서 인증 상태 업데이트
            self.repository.update_verification_status(user_id, phone_number, True)
            return True
        else:
            return False
