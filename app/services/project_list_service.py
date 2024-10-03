# app/services/project_list_service.py

# 필요한 모듈을 불러옵니다
from app.repositories.project_list_repository import ProjectRepository

class ProjectService:
    def __init__(self, project_repository):
        self.project_repository = project_repository

    def get_project(self, project_id):
        return self.project_repository.find_by_id(project_id)

    def get_all_projects(self):
        return self.project_repository.find_all()

    def create_project(self, project_data):
        return self.project_repository.create(project_data)

    def update_project(self, project_id, project_data):
        return self.project_repository.update(project_id, project_data)

    def delete_project(self, project_id):
        return self.project_repository.delete(project_id)

