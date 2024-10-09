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
from twilio.rest import Client


class IdentityVerificationService:
    def __init__(self):
        self.repository = IdentityVerificationRepository()

        # Twilio API 설정
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

        # Twilio 클라이언트 생성
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)

    def send_verification_code(self, phone_number):
        # 랜덤 6자리 인증 코드 생성
        verification_code = f"{random.randint(100000, 999999)}"
        expiration_time = datetime.utcnow() + timedelta(minutes=5)  # 인증 코드 5분 후 만료

        # 도메인 객체 생성 및 전화번호 유효성 검사
        domain = IdentityVerificationDomain(phone_number, verification_code, expiration_time)
        if not domain.is_valid_phone_number():
            raise ValueError("잘못된 전화번호 형식입니다")

        # Twilio API를 사용하여 SMS 전송
        try:
            message = self.client.messages.create(
                body=f"인증번호 [{verification_code}]를 입력해 주세요.",
                from_=self.twilio_phone_number,
                to=phone_number
            )
            
            if not message.sid:
                raise Exception("SMS 전송 실패")
            
        except Exception as e:
            raise Exception(f"Twilio 오류: {str(e)}")

        # 레포지토리에 저장 (DB)
        self.repository.save_verification(phone_number, verification_code, expiration_time)

    def verify_code(self, user_id, phone_number, input_code):
        # 레포지토리에서 인증 정보 가져오기
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
