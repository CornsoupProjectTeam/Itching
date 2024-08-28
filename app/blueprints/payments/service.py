import requests
import os
import base64
from dotenv import load_dotenv
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from .domain import PayPalPayment, TossPayment

# .env 파일 로드
load_dotenv()

# PayPal 환경 설정 (샌드박스 또는 라이브 환경)
client_id = os.getenv("PAYPAL_CLIENT_ID")
client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

# 환경 변수 유효성 확인
if not client_id or not client_secret:
    raise ValueError("PayPal client ID and secret must be set in the environment variables.")

environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)

class PayPalPaymentService:
    @staticmethod
    def create_payment(total, currency="USD", description="Payment"):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        
        request.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(total)
                },
                "description": description
            }],
            "application_context": {
                "return_url": "http://localhost:5000/payment/success",
                "cancel_url": "http://localhost:5000/payment/cancel"
            }
        })

        try:
            # PayPal API에 결제 요청 보내기
            response = client.execute(request)
            for link in response.result.links:
                if link.rel == "approve":
                    # PayPal 승인 URL을 반환
                    return link.href
        except IOError as ioe:
            # 에러 처리
            print(f"PayPal Create Payment Error: {ioe}")
        return None

    @staticmethod
    def execute_payment(payment_id):
        request = OrdersCaptureRequest(payment_id)
        try:
            response = client.execute(request)
            return response.result.status == "COMPLETED"
        except IOError as ioe:
            # 에러 처리
            print(f"PayPal Execute Payment Error: {ioe}")
        return False

# TossPayments 설정
class TossPaymentService:
    TOSS_API_URL = "https://api.tosspayments.com/v1/payments"
    TOSS_SECRET_KEY = os.getenv("TOSS_SECRET_KEY")

    # 환경 변수 유효성 확인
    if not TOSS_SECRET_KEY:
        raise ValueError("TOSS_SECRET_KEY must be set in the environment variables.")

    @staticmethod
    def _get_authorization_header():
        # TossPayments의 secret_key를 Base64로 인코딩하여 Authorization 헤더 생성
        encoded_secret_key = base64.b64encode(f"{TossPaymentService.TOSS_SECRET_KEY}:".encode()).decode()
        return f"Basic {encoded_secret_key}"

    @staticmethod
    def create_payment(payment_data):
        headers = {
            "Authorization": TossPaymentService._get_authorization_header(),
            "Content-Type": "application/json"
        }

        # 디버깅용으로 요청 데이터 출력
        print("Requesting Toss Payments API with data:", payment_data)

        # TossPayments 결제 생성 요청
        response = requests.post(TossPaymentService.TOSS_API_URL, json=payment_data, headers=headers)
        
        # 응답 상태 코드와 데이터 출력
        print(f"Toss Payments API Response Status Code: {response.status_code}")
        print(f"Toss Payments API Response Data: {response.json()}")
        
        response_data = response.json()

        # 결제 생성이 성공했으면 승인 URL 반환
        if response.status_code == 200:
            return response_data.get('nextRedirectAppUrl') or response_data.get('nextRedirectPcUrl')
        else:
            # 에러 로그 추가
            print(f"Toss Create Payment Error: {response.status_code}, {response_data}")
            return None

    @staticmethod
    def execute_payment(payment_key, order_id, amount):
        url = f"{TossPaymentService.TOSS_API_URL}/confirm"
        headers = {
            "Authorization": TossPaymentService._get_authorization_header(),
            "Content-Type": "application/json"
        }
        data = {
            "paymentKey": payment_key,
            "orderId": order_id,
            "amount": amount
        }

        # TossPayments 결제 완료 요청
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return True, response.json()
        else:
            # 에러 로그 추가
            print(f"Toss Execute Payment Error: {response.status_code}, {response.json()}")
            return False, response.json()
