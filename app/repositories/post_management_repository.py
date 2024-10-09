from sqlalchemy.exc import SQLAlchemyError
from app.models.post_management import PostManagement, db
from app.models.client_explore import ClientPost

class PostManagementRepository:

    def save_post_management(self, post_info:PostManagement) -> dict:
        try:
            db.session.add(post_info)
            db.session.commit()
            return {'success': True}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def get_posts_by_user_id(self, user_id: str) -> list[PostManagement]:
        try:
            posts = PostManagement.query.filter_by(user_id=user_id).all()
            return posts
        except SQLAlchemyError as e:
            return None
    
    def delete_post_management(self, post_id: str) -> dict:
        try:
            # post_id가 PST로 시작하는 경우 ClientPost 테이블에서 삭제
            if post_id.startswith('PST'):
                client_post = ClientPost.query.filter_by(client_post_id=post_id).first()
                if client_post:
                    db.session.delete(client_post)

            # PostManagement 테이블에서 reference_post_id가 post_id와 일치하는 행 삭제
            post_management_entry = PostManagement.query.filter_by(reference_post_id=post_id).first()
            if post_management_entry:
                db.session.delete(post_management_entry)

            # 트랜잭션 커밋
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def get_reference_post_id_by_post_id(self, post_id: str) -> str:
        try:
            post = PostManagement.query.filter_by(post_id=post_id).first()
            return post.reference_post_id if post else None
        except SQLAlchemyError as e:
            return None