# app/routes/project_list_routes.py
from flask import Blueprint, render_template
from app.models.project_list import ProjectList

project_list_bp = Blueprint('project_list', __name__)

@project_list_bp.route('/projects', methods=['GET'])
def show_projects():
    # 데이터베이스에서 모든 프로젝트 데이터를 가져오기
    projects = ProjectList.query.all()
    
    # 데이터를 템플릿으로 전달하여 HTML 페이지에서 출력
    return render_template('project_list.html', projects=projects)


