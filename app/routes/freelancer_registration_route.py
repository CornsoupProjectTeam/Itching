from flask import Blueprint, request, jsonify, g
from app.services.freelancer_registration_service import FreelancerRegistrationService
from app.repositories.freelancer_registration_repository import FreelancerRegistrationRepository
from app.services.user_information_service import UserInformationService
from app.repositories.user_information_repository import UserInformationRepository

freelancer_registration_bp = Blueprint('freelancer_registration', __name__, url_prefix='/profile/freelancer')

@freelancer_registration_bp.before_request
def before_request():
    g.freelancer_registration_repository = FreelancerRegistrationRepository()
    g.userinformation_repository = UserInformationRepository()
    g.userinformation_service = UserInformationService(g.userinformation_repository, request.view_args.get('user_id'))
    
    g.freelancer_registration_service = FreelancerRegistrationService(
        g.freelancer_registration_repository, 
        g.userinformation_service, 
        request.view_args.get('user_id')
    )

# GET /profile/freelancer/{user_id}/register
# 프리랜서 등록 정보 조회
@freelancer_registration_bp.route('/<user_id>/register', methods=['GET'])
def get_freelancer_registration(user_id):
    result = g.freelancer_registration_service.get_freelancer_registration_information()
    
    # 등록 정보가 있는 경우 JSON으로 반환
    if result:
        return jsonify({"success": True, "data": result}), 200
    else:
        return jsonify({"success": False, "message": "등록 정보를 찾을 수 없습니다."}), 404

# POST 또는 DELETE /profile/freelancer/{user_id}/register/profile-image
@freelancer_registration_bp.route('/<user_id>/register/profile-image', methods=['POST', 'DELETE'])
def update_profile_image(user_id):
    # 프로필 사진 등록/업데이트
    if request.method == 'POST':        
        file = request.files.get('file')

        # 파일이 없으면 오류 반환
        if not file:
            return jsonify({"success": False, "message": "파일이 제공되지 않았습니다."}), 400

        # 프로필 사진 변경 처리
        result = g.freelancer_registration_service.change_profile_picture(user_id, file)

        # 결과 반환
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    # 프로필 사진 삭제
    elif request.method == 'DELETE':
        # 파일을 None으로 설정하여 삭제 로직 수행
        result = g.freelancer_registration_service.change_profile_picture(user_id, None)

        # 결과 반환
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

# POST 또는 PUT /profile/freelancer/{user_id}/register/freelancer-intro
# 프리랜서 소개 등록 수정
@freelancer_registration_bp.route('/<user_id>/register/freelancer-intro', methods=['POST', 'PUT'])
def update_freelancer_intro(user_id):
    intro_text = request.json.get('freelancer_intro')
    result = g.freelancer_registration_service.update_freelancer_intro(user_id, intro_text)
    return jsonify(result)

# POST 또는 PUT /profile/freelancer/{user_id}/register/expertise-fields
# 전문 분야 선택 등록 및 수정
@freelancer_registration_bp.route('/<user_id>/register/expertise-fields', methods=['POST', 'PUT'])
def update_expertise_fields(user_id):
    field_codes = request.json.get('field_codes')
    
    # POST 요청인 경우: 새로운 전문 분야 추가
    if request.method == 'POST':
        result = g.freelancer_registration_service.update_expertise_fields(user_id, field_codes, None)
    
    # PUT 요청인 경우: 전문 분야 수정 (추가 및 삭제)
    elif request.method == 'PUT':
        deleted_field_codes = request.json.get('deleted_field_codes')
        result = g.freelancer_registration_service.update_expertise_fields(user_id, field_codes, deleted_field_codes)
    
    return jsonify(result)

# POST 또는 PUT /profile/freelancer/{user_id}/register/skill-codes
# 보유 기술 입력 등록
@freelancer_registration_bp.route('/<user_id>/register/skill-codes', methods=['POST', 'PUT'])
def update_skill_codes(user_id):
    skill_codes = request.json.get('skill_codes')
    
    # POST 요청인 경우: 새로운 스킬 코드 추가
    if request.method == 'POST':
        result = g.freelancer_registration_service.update_skill_codes(user_id, skill_codes, None)
    
    # PUT 요청인 경우: 스킬 코드 수정 (추가 및 삭제)
    elif request.method == 'PUT':
        deleted_skill_codes = request.json.get('deleted_skill_codes')
        result = g.freelancer_registration_service.update_skill_codes(user_id, skill_codes, deleted_skill_codes)
    
    return jsonify(result)

#POST 또는 PUT /profile/freelancer/{user_id}/register/educations
# 학력 사항 입력 등록
@freelancer_registration_bp.route('/<user_id>/register/educations', methods=['POST', 'PUT'])
def update_educations(user_id):
    schools = request.json.get('schools')
    
    # POST 요청인 경우: 새로운 학력 추가
    if request.method == 'POST':
        result = g.freelancer_registration_service.update_educations(user_id, schools, None)
    
    # PUT 요청인 경우: 학력 수정 (추가 및 삭제)
    elif request.method == 'PUT':
        deleted_schools = request.json.get('deleted_schools')
        result = g.freelancer_registration_service.update_educations(user_id, schools, deleted_schools)
    
    return jsonify(result)

# POST 또는 PUT /profile/freelancer/{user_id}/register/careers
# 경력 사항 입력 등록
@freelancer_registration_bp.route('/<user_id>/register/careers', methods=['POST', 'PUT'])
def update_careers(user_id):
    careers = request.json.get('careers')
    
    # POST 요청인 경우: 새로운 경력 추가
    if request.method == 'POST':
        result = g.freelancer_registration_service.update_careers(user_id, careers, None)
    
    # PUT 요청인 경우: 경력 수정 (추가 및 삭제)
    elif request.method == 'PUT':
        deleted_careers = request.json.get('deleted_careers')
        result = g.freelancer_registration_service.update_careers(user_id, careers, deleted_careers)
    
    return jsonify(result)

# POST 또는 PUT /profile/freelancer/{user_id}/register/sns-link
# SNS 계정 등록 수정
@freelancer_registration_bp.route('/<user_id>/register/sns-link', methods=['POST', 'PUT'])
def update_sns_link(user_id):
    sns_link = request.json.get('sns_link')
    result = g.freelancer_registration_service.update_sns_link(user_id, sns_link)
    return jsonify(result)

# POST 또는 DELETE /profile/freelancer/{user_id}/register/portfolios
# 포트폴리오 등록/삭제
@freelancer_registration_bp.route('/<user_id>/register/portfolios', methods=['POST', 'DELETE'])
def update_portfolios(user_id):
    # POST 요청인 경우: 포트폴리오 이미지 업로드
    if request.method == 'POST':
        portfolio_images = request.files.getlist('portfolio_images')  # 다중 파일 업로드 처리
        result = g.freelancer_registration_service.update_portfolios(user_id, portfolio_images, None)
    
    # DELETE 요청인 경우: 포트폴리오 이미지 삭제
    elif request.method == 'DELETE':
        deleted_portfolio_image_paths = request.json.get('deleted_portfolio_image_paths')  # 삭제할 이미지 경로 리스트
        result = g.freelancer_registration_service.update_portfolios(user_id, None, deleted_portfolio_image_paths)
    
    return jsonify(result)

# GET /profile/freelancer/{user_id}/register/complete
# 프리랜서 등록의 필수 항목이 모두 저장되었는지 확인
@freelancer_registration_bp.route('/<user_id>/register/complete', methods=['GET'])
def check_registration_complete(user_id):
    result = g.freelancer_registration_service.registration_complete(user_id)
    
    return jsonify(result)
