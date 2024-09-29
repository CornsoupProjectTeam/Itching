from flask import Blueprint, request, jsonify
from app.services.user_information_service import UserInformationService
from app.repositories.user_information_repository import UserInformationRepository
from app.services.login_service import LoginService
from app.repositories.login_repository import LoginRepository

user_information_bp = Blueprint('user_information', __name__, url_prefix='/main/profile/user_information')

user_information_repository = UserInformationRepository()
login_repository = LoginRepository()

# 경로 : /main/profile/user_information/{user_id}
@user_information_bp.route('/<user_id>', methods=['GET'])
def get_user_information(user_id):    
    user_info_service = UserInformationService(user_information_repository, user_id)
    user_info = user_info_service.get_user_information()
    if not user_info:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404

    return jsonify(user_info)

# 경로 : /main/profile/user_information/{user_id}/image-change
@user_information_bp.route('/<user_id>/image-change', methods=['POST', 'DELETE'])
def change_profile_image(user_id):
    # POST: 이미지 업로드, DELETE: 이미지 삭제
    if request.method == 'POST':
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({'error': '이미지 파일이 제공되지 않았습니다.'}), 400
    else:
        # DELETE 요청일 경우
        image_file = None

    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_profile_picture(user_id, image_file)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/nickname-change
@user_information_bp.route('/<user_id>/nickname/change', methods=['PUT'])
def change_nickname(user_id):
    new_nickname = request.json.get('new_nickname')
    if not new_nickname:
        return jsonify({'error': '새로운 닉네임이 필요합니다.'}), 400
    
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.change_nickname(user_id, new_nickname)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/business/update
@user_information_bp.route('/<user_id>/business/update', methods=['PUT'])
def update_business_area(user_id):
    new_business_area = request.json.get('new_business_area')
    if not new_business_area:
        return jsonify({'error': '새로운 비즈니스 정보가 필요합니다.'}), 400
    
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.save_new_business(user_id, new_business_area)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/interests/update
@user_information_bp.route('/<user_id>/interests/update', methods=['PUT'])
def update_interests(user_id):
    new_interests = request.json.get('new_interests')
    if not new_interests:
        return jsonify({'error': '새로운 관심사 정보가 필요합니다.'}), 400
    
    user_info_service = UserInformationService(user_information_repository, user_id)
    result = user_info_service.save_new_interest(user_id, new_interests)
    return jsonify(result)

# 경로 : /main/profile/user_information/{user_id}/password-change
@user_information_bp.route('/<user_id>/password-change', methods=['PUT'])
def change_password(user_id):
    # 프론트엔드에서 전달받은 현재 비밀번호, 새 비밀번호, 비밀번호 확인
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    confirm_new_password = request.json.get('confirm_new_password')

    if not current_password or not new_password or not confirm_new_password:
        return jsonify({'error': '현재 비밀번호, 새 비밀번호, 비밀번호 확인이 필요합니다.'}), 400

    # LoginService를 통해 비밀번호 변경 요청 처리
    login_service = LoginService(login_repository)
    result = login_service.change_password(user_id, current_password, new_password, confirm_new_password)
    return jsonify(result)