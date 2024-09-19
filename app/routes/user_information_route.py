from flask import Blueprint, request, jsonify
from app.services.user_information_service import UserInformationService
from app.repositories.user_information_repository import UserInformationRepository

user_information_bp = Blueprint('user_information', __name__, url_prefix='/main/profile/user_information')

user_information_repository = UserInformationRepository()

# 경로 : /main/profile/user_information/{user_id}
@user_information_bp.route('/<user_id>', methods=['GET'])
def get_user_information(user_id):
    
    # 서비스 레이어를 통해 user_id로 사용자 정보 조회
    user_info_service = UserInformationService(user_information_repository, user_id)
    user_info = user_info_service.get_user_information()
    if not user_info:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user_info)

# 경로 : /main/profile/user_information/{user_id}/image/upload
@user_information_bp.route('/<user_id>/image/upload', methods=['POST'])
def upload_image(user_id):
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({'error': 'No image file provided'}), 400
    
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_profile_picture.upload_profile_picture(user_id, image_file)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/image/delete
@user_information_bp.route('/<user_id>/image/delete', methods=['DELETE'])
def delete_image(user_id):
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_profile_picture.delete_profile_picture(user_id)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/nickname/check
@user_information_bp.route('/<user_id>/nickname/check', methods=['POST'])
def check_nickname(user_id):
    nickname = request.json.get('nickname')
    if not nickname:
        return jsonify({'error': 'Nickname is required'}), 400

    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_nickname.validate_nickname(nickname)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/nickname/change
@user_information_bp.route('/<user_id>/nickname/change', methods=['PUT'])
def change_nickname(user_id):
    new_nickname = request.json.get('new_nickname')
    if not new_nickname:
        return jsonify({'error': 'New nickname is required'}), 400
    
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_nickname.save_new_nickname(user_id, new_nickname)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/business/update
@user_information_bp.route('/<user_id>/business/update', methods=['PUT'])
def update_business_area(user_id):
    new_business_area = request.json.get('new_business_area')
    
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_business.save_new_business(user_id, new_business_area)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/interests/update
@user_information_bp.route('/<user_id>/interests/update', methods=['PUT'])
def update_interests(user_id):
    new_interests = request.json.get('new_interests')
    
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_interest.save_new_interest(user_id, new_interests)
    return jsonify(result)
