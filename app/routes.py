from flask import Flask, jsonify, send_from_directory, render_template, request
from app import app
import os
from app.blueprints.payments import payments_bp

# API 엔드포인트 예시
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello from Flask!",
        "status": "success"
    }
    return jsonify(data)

# React 정적 파일 제공 (index.html 등)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and path.startswith("static"):
        return send_from_directory(app.static_folder, path)
    elif path.endswith(".js") or path.endswith(".css") or path.endswith(".ico"):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
# 결제 페이지
@payments_bp.route('/payment', methods=['GET'])
def payment_page():
    return render_template('payments.html')

# 결제 성공 라우트
@payments_bp.route('/payment/success', methods=['GET'])
def payment_success():
    # 결제가 성공한 경우 성공 메시지를 전달
    return render_template('paymentResult.html', message="Payment was successful!")

# 결제 실패 라우트
@payments_bp.route('/payment/fail', methods=['GET'])
def payment_fail():
    # 결제가 실패한 경우 실패 메시지를 전달
    return render_template('paymentResult.html', message="Payment failed. Please try again.")
