# app/services/client_post_service.py

from app.repositories.client_post_repository import ClientPostRepository
from typing import List, Optional
from app.domain.client_post_domain import ClientPost

class ClientPostService:
    def __init__(self, client_post_repository: ClientPostRepository):
        self.client_post_repository = client_post_repository

    def get_client_post_by_id(self, client_post_id: str) -> Optional[ClientPost]:
        """특정 클라이언트 게시물을 ID로 조회"""
        return self.client_post_repository.find_by_id(client_post_id)

    def get_all_client_posts(self) -> List[ClientPost]:
        """모든 클라이언트 게시물 조회"""
        return self.client_post_repository.find_all()

    def save_client_post(self, client_post: ClientPost) -> bool:
        """클라이언트 게시물 저장"""
        return self.client_post_repository.save(client_post)
