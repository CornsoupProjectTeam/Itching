# app/routes/freelancer_list_routes.py

from flask import Blueprint, render_template
from app.services.freelancer_list_service import FreelancerProfileService
from app.repositories.freelancer_list_repository import FreelancerProfileRepository

# 라우터 설정
freelancer_bp = Blueprint('freelancer', __name__)

# 레포지토리와 서비스 초기화
freelancer_repository = FreelancerProfileRepository()
freelancer_service = FreelancerProfileService(freelancer_repository)

@freelancer_bp.route('/', methods=['GET'])
def list_freelancers():
    """모든 프리랜서 목록을 HTML 템플릿에 출력"""
    freelancers = freelancer_service.get_all_freelancers()
    return render_template('freelancer_list.html', freelancers=freelancers)
