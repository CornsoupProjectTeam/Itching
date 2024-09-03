from flask import render_template, redirect, url_for, request, jsonify
from . import payments_bp
from .service import PayPalPaymentService, TossPaymentService
from .domain import PayPalPayment, TossPayment
import uuid

# 결제 생성 페이지
@payments_bp.route('/payment/create', methods=['POST'])
def pay():
    data = request.get_json()  # JSON 데이터로 받음
    payment_method = data.get('payment_method')

    # 서버에서 아이템 데이터 생성 (레포지토리 대신 임시 하드코딩된 데이터 사용)
    items = [{
        "name": "Sample Item",
        "price": "10",  # 가격 (Toss는 원화, PayPal은 달러를 기준으로 설정)
        "currency": "KRW" if payment_method == 'toss' else "USD",
        "quantity": 1
    }]

    if payment_method == 'toss':
        # TossPayments 결제 처리
        
        order_id = str(uuid.uuid4()) # 서버에서 order_id 생성
        customer_name = "YujinChoi"  # 사용자 이름 하드코딩

        payment = TossPayment(items=items, order_id=order_id, customer_name=customer_name)
        payment_data = payment.to_toss_dict()

        # 개별 필드 로그 출력
        print(f"Order ID: {order_id}")
        print(f"Customer Name: {customer_name}")
        print(f"Amount: {payment_data['amount']}")
        print(f"Order Name: {payment_data['orderName']}")

        return jsonify({
            "amount": payment_data["amount"],
            "orderId": payment_data["orderId"],
            "orderName": payment_data["orderName"],
            "customerName": payment_data["customerName"]
        }), 200

    elif payment_method == 'paypal':
        # PayPal 결제 처리
        total = sum(float(item['price']) * item['quantity'] for item in items)  # 총액 계산
        approval_url = PayPalPaymentService.create_payment(total, currency='USD')

        if approval_url:
            return jsonify({"approval_url": approval_url}), 200  # 승인 URL을 JSON으로 반환
        else:
            return jsonify({"error": "Error while creating PayPal payment"}), 500

    else:
        return jsonify({"error": "Invalid payment method"}), 400

@payments_bp.route('/payment/execute', methods=['POST'])
def payment_execute():
    data = request.get_json()  # JSON 데이터로 받음
    payment_method = data.get('payment_method')

    if payment_method == 'toss':
        payment_key = data.get('paymentKey')
        order_id = data.get('orderId')
        amount = data.get('amount')

        success, response = TossPaymentService.execute_payment(payment_key, order_id, amount)

        if success:
            return jsonify({"message": "Toss payment executed successfully", "details": response}), 200
        else:
            return jsonify({"error": "Toss payment execution failed", "details": response}), 500

    elif payment_method == 'paypal':
        payment_id = data.get('paymentId')

        if PayPalPaymentService.execute_payment(payment_id):
            return jsonify({"message": "PayPal payment executed successfully"}), 200
        else:
            return jsonify({"error": "PayPal payment execution failed"}), 500

    else:
        return jsonify({"error": "Invalid payment method"}), 400

@payments_bp.route('/payment', methods=['GET'])
def payment_page():
    return render_template('payments.html')

@payments_bp.route('/payment/success', methods=['GET'])
def payment_success():
    return render_template('paymentResult.html', message="Payment was successful!")

@payments_bp.route('/payment/fail', methods=['GET'])
def payment_fail():
    return render_template('paymentResult.html', message="Payment failed. Please try again.")