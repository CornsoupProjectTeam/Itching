# app/repositories/client_post_repository.py

from app.models.client_post_list import ClientPostList
from app.domain.client_post_domain import ClientPost
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List

class ClientPostRepository:
    def find_by_id(self, client_post_id: str) -> Optional[ClientPost]:
        """주어진 게시물 ID로 게시물 정보를 조회합니다."""
        try:
            post_data = ClientPostList.query.filter_by(client_post_id=client_post_id).first()
            if post_data:
                return self._convert_to_domain(post_data)
            return None
        except SQLAlchemyError as e:
            print(f"Error retrieving client post by ID: {e}")
            return None

    def find_all(self) -> List[ClientPost]:
        """모든 클라이언트 게시물 정보를 조회합니다."""
        try:
            posts_data = ClientPostList.query.all()
            return [self._convert_to_domain(post) for post in posts_data]
        except SQLAlchemyError as e:
            print(f"Error retrieving all client posts: {e}")
            return []

    def _convert_to_domain(self, post_data) -> ClientPost:
        """SQLAlchemy 모델을 도메인 객체로 변환합니다."""
        return ClientPost(
            client_post_id=post_data.client_post_id,
            client_user_id=post_data.client_user_id,
            field_code=post_data.field_code,
            title=post_data.client_title,
            payment_amount=post_data.client_payment_amount,
            desired_deadline=post_data.desired_deadline,
            created_at=post_data.created_at,
            updated_at=post_data.updated_at
        )

    def _convert_to_model(self, client_post: ClientPost):
        """도메인 객체를 SQLAlchemy 모델로 변환합니다."""
        post_data = ClientPostList.query.filter_by(client_post_id=client_post.client_post_id).first()

        if not post_data:
            post_data = ClientPostList(
                client_post_id=client_post.client_post_id,
                created_at=client_post.created_at
            )

        post_data.client_user_id = client_post.client_user_id
        post_data.field_code = client_post.field_code
        post_data.client_title = client_post.title
        post_data.client_payment_amount = client_post.payment_amount
        post_data.desired_deadline = client_post.desired_deadline
        post_data.updated_at = client_post.updated_at

        return post_data
