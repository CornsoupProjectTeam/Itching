#payment_authentication_route.py

from flask import Blueprint, request, jsonify
from app.services.payment_authentication_service import AuthenticationService

payment_authentication_bp = Blueprint('authentication', __name__)

@payment_authentication_bp.route('/payment/check', methods=['POST'])
def authenticate_user():
    data = request.json
    user_name = data.get('user_name')
    client_user_id = data.get('client_user_id')
    password = data.get('password')

    is_authenticated, message = AuthenticationService.authenticate(user_name, client_user_id, password)

    if is_authenticated:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 401
