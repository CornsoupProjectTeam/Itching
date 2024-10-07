# app/routes/image_upload.py

from flask import Blueprint, request, jsonify
from app.utils.image_upload import upload_image, delete_image

image_upload_bp = Blueprint('image_upload', __name__)

@image_upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    user_id = request.form.get('user_id')

    # 파일 업로드 유틸 호출
    random_filename, error = upload_image(file, user_id)
    
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'filename': random_filename}), 200

@image_upload_bp.route('/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    user_id = data.get('user_id')
    filename = data.get('filename')

    success, error = delete_image(user_id, filename)
    
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'success': True}), 200