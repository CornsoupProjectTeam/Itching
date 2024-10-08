from flask import Blueprint, request, jsonify, g
from app.services.freelancer_information_service import FreelancerInformationService
from app.repositories.freelancer_information_repository import FreelancerInformationRepository
from app.services.freelancer_registration_service import FreelancerRegistrationService
from app.repositories.freelancer_registration_repository import FreelancerRegistrationRepository
from app.services.user_information_service import UserInformationService
from app.repositories.user_information_repository import UserInformationRepository

freelancer_information_bp = Blueprint('freelancer_information', __name__, url_prefix='/profile/freelancer')

@freelancer_information_bp.before_request
def before_request():
    # 각 서비스 및 리포지토리 객체 생성 및 g에 바인딩
    g.user_information_repository = UserInformationRepository()
    g.freelancer_information_repository = FreelancerInformationRepository()
    g.freelancer_registration_repository = FreelancerRegistrationRepository()
    
    # user_information_service 생성 시 필요한 인수를 전달
    g.user_information_service = UserInformationService(
        g.user_information_repository,
        request.view_args.get('freelancer_user_id')
    )
    g.freelancer_registration_service = FreelancerRegistrationService(
        g.freelancer_registration_repository,
        g.user_information_service,
        request.view_args.get('freelancer_user_id')
    )
    g.freelancer_service = FreelancerInformationService(
        g.freelancer_information_repository,
        g.freelancer_registration_service,
        request.view_args.get('freelancer_user_id')
    )

# GET /profile/freelancer/{freelancer_user_id}/public-profile
@freelancer_information_bp.route('/<freelancer_user_id>/public-profile', methods=['GET'])
def get_freelancer_information(freelancer_user_id):
    # Freelancer Registration 정보 가져오기
    registration_result = g.freelancer_registration_service.get_freelancer_registration_information()
    
    # Freelancer Information 정보 가져오기
    information_result = g.freelancer_service.get_freelancer_information()

    # 두 결과 통합
    if registration_result and information_result:
        combined_result = {
            "registration_info": {
                "public_profile_id": registration_result["public_profile_id"],
                "user_id": registration_result["user_id"],
                "profile_image_path": registration_result["profile_image_path"],
                "freelancer_intro": registration_result["freelancer_intro"],
                "expertise_fields": registration_result["expertise_fields"],
                "skill_codes": registration_result["skill_codes"],
                "educations": registration_result["educations"],
                "careers": registration_result["careers"],
                "portfolios": registration_result["portfolios"],
                "sns_link": registration_result["sns_link"],
                "freelancer_registration_date": registration_result["freelancer_registration_date"],
                "freelancer_badge": registration_result["freelancer_badge"]
            },
            "additional_info": {
                "freelancer_badge": information_result["freelancer_badge"],
                "match_count": information_result["match_count"],
                "freelancer_intro_one_liner": information_result["freelancer_intro_one_liner"],
                "project_duration": information_result["project_duration"],
                "public_profile_registration_st": information_result["public_profile_registration_st"],
                "service_options": information_result["service_options"],
                "price_range": information_result["price_range"],
                "preferred_work_style": information_result["preferred_work_style"],
                "account_info": information_result["account_info"],
                "review": information_result["review"],
                "review_summary": information_result["review_summary"]
            }
        }
        return combined_result, 200

    # 실패한 경우
    return jsonify({"success": False, "message": "프로필 정보를 불러올 수 없습니다."}), 404

# PUT /profile/freelancer/{freelancer_user_id}/public-profile
@freelancer_information_bp.route('/<freelancer_user_id>/public-profile', methods=['PUT'])
def save_freelancer_additional_information(freelancer_user_id):
    data = request.json

    # 각 데이터 그룹별로 처리
    public_profile = data.get('public_profile', {})
    service_options = data.get('service_options', {})
    price_info = data.get('price_range', {})
    account_info = data.get('account_information', {})
    preferred_work_style = data.get('preferred_work_style', {})

    # 각각의 추가 정보 업데이트
    project_duration_result = g.freelancer_service.update_project_duration(public_profile.get('project_duration'))
    intro_result = g.freelancer_service.update_freelancer_intro_one_liner(public_profile.get('intro_one_liner'))

    service_options_result = g.freelancer_service.update_serviceoptions(
        service_options.get('weekend_consultation'), 
        service_options.get('weekend_work')
    )
    
    price_range_result = g.freelancer_service.update_price_range(
        price_info.get('min_price'), 
        price_info.get('max_price'), 
        price_info.get('price_unit')
    )
    
    account_info_result = g.freelancer_service.update_account_info(
        account_info.get('bank_name'), 
        account_info.get('account_number'), 
        account_info.get('account_holder'), 
        account_info.get('account_type')
    )
    
    preferred_work_style_result = g.freelancer_service.update_preferred_work_style(
        preferred_work_style.get('preferred_codes'), 
        preferred_work_style.get('deleted_preferred_codes')
    )
    
    # 모든 업데이트가 성공적으로 이루어졌는지 확인
    if all([project_duration_result['success'], intro_result['success'], service_options_result['success'],
            price_range_result['success'], account_info_result['success'], preferred_work_style_result['success']]):
        return jsonify({"success": True, "message": "추가 정보가 성공적으로 저장되었습니다."})
    else:
        return jsonify({"success": False, "message": "추가 정보 저장 중 오류가 발생했습니다."})

# PUT /profile/freelancer/{freelancer_user_id}/public-profile/registration-state
@freelancer_information_bp.route('/<freelancer_user_id>/public-profile/registration-state', methods=['PUT'])
def update_public_profile_registration_st(freelancer_user_id):
    data = request.json
    registration_state = data.get('registration_state')
    result = g.freelancer_service.update_public_profile_registration_st(registration_state)
    return jsonify(result)

# POST /profile/freelancer/{freelancer_user_id}/public-profile/reviews
@freelancer_information_bp.route('/<freelancer_user_id>/public-profile/reviews', methods=['POST'])
def add_review(freelancer_user_id):
    data = request.json
    review_title = data.get('review_title')
    review_text = data.get('review_text')
    rating = data.get('rating')
    client_user_id = data.get('client_user_id')
    result = g.freelancer_service.add_review(freelancer_user_id, review_title, review_text, rating, client_user_id)
    return jsonify(result)

# DELETE /profile/freelancer/{freelancer_user_id}/public-profile/reviews
@freelancer_information_bp.route('/<freelancer_user_id>/public-profile/reviews', methods=['DELETE'])
def delete_review(freelancer_user_id):
    data = request.json
    review_title = data.get('review_title')
    review_text = data.get('review_text')
    rating = data.get('rating')
    client_user_id = data.get('client_user_id')
    result = g.freelancer_service.delete_review(freelancer_user_id, review_title, review_text, rating, client_user_id)
    return jsonify(result)

# GET /profile/freelancer/public_profile_id}/public-profile/list
# 나중에 프리랜서 탐색으로 옮길 것
# @freelancer_information_bp.route('/<public_profile_id>/profile-list', methods=['GET'])
# def get_public_profile_list(public_profile_id):
#     result = g.freelancer_service.get_public_profile_list(public_profile_id)
#     return jsonify(result)
