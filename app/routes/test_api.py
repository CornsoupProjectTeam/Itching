from flask import Blueprint, jsonify

test_api_bp = Blueprint('api', __name__)

@test_api_bp.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello from Flask!",
        "status": "success"
    }
    return jsonify(data)
