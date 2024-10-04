#app/repositories/project_list_repository.py
import app.models.project_info
import app.models.project_list
import app.domain.project_list_domain

# 명시적으로 클래스 임포트
from app.models.project_info import ProjectInfo
from app.domain.project_list_domain import Project

class ProjectRepository:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, project_id):
        # ProjectInfo 모델에서 데이터를 쿼리
        project_data = ProjectInfo.query.filter_by(project_id=project_id).first()
        if project_data:
            # Project 도메인 객체로 변환
            return Project(
                project_data.project_id, 
                project_data.public_profile_id, 
                project_data.field_code, 
                project_data.project_title, 
                project_data.project_payment_amount, 
                project_data.design_draft_count, 
                project_data.production_time, 
                project_data.commercial_user_allowed, 
                project_data.high_resolution_file_available, 
                project_data.delivery_routes, 
                project_data.additional_notes, 
                project_data.cancellation_and_refund_policy, 
                project_data.product_info_disclosure, 
                project_data.additional_info, 
                project_data.created_at, 
                project_data.updated_at
            )
        return None



