from app.models.client_explore import *
from sqlalchemy.exc import SQLAlchemyError

class ClientExploreRepository:
    def get_client_post_information(self, client_post_id: str) -> dict:
        client_post = ClientPost.query.filter_by(client_post_id=client_post_id).first()

        if not client_post:
            return {'success': False, 'message': '클라이언트 글이 없습니다.'}
        
        # 매핑 테이블에서 client_reference_image_mapping 정보 가져오기
        client_reference_image_mapping = ClientPostReferenceImageMapping.query.filter_by(client_post_id=client_post_id).all()

        return {
            "client_post_id": client_post.client_post_id,
            "client_user_id": client_post.client_user_id,
            "field_code": client_post.field_code,
            "client_title": client_post.client_title,
            "client_payment_amount": client_post.client_payment_amount,
            "completion_deadline": client_post.completion_deadline,
            "posting_deadline": client_post.posting_deadline,
            "requirements": client_post.requirements,
            "client_reference_image_mapping": client_reference_image_mapping
        }

    def filter_client_posts(self, min_price, max_price, deadline_date, field_code):
        query = ClientPostList.query

        # 필터링 조건 적용
        if min_price is not None:
            query = query.filter(ClientPostList.client_payment_amount >= min_price)
        if max_price is not None:
            query = query.filter(ClientPostList.client_payment_amount <= max_price)
        if deadline_date is not None:
            query = query.filter(ClientPostList.desired_deadline <= deadline_date)
        if field_code is not None:
            query = query.filter(ClientPostList.field_code == field_code)

        return query.all()

    def get_all_client_posts(self):
        # 필터링 조건 없이 모든 클라이언트 데이터 가져오기
        return ClientPostList.query.all()

    def sort_client_posts(self, client_posts, sort_field, order):
        # 정렬 조건 적용
        if order == 'asc':
            return sorted(client_posts, key=lambda x: getattr(x, sort_field))
        else:
            return sorted(client_posts, key=lambda x: getattr(x, sort_field), reverse=True)

    def create_client_post(self, client_post_id, client_user_id, client_post_info):
        try:
            # 새로운 클라이언트 글 생성
            client_post = ClientPost(
                client_post_id=client_post_id,
                client_user_id=client_user_id,
                field_code=client_post_info.get('field_code'),
                client_title=client_post_info.get('client_title'),
                client_payment_amount=client_post_info.get('client_payment_amount'),
                completion_deadline=client_post_info.get('completion_deadline'),
                posting_deadline=client_post_info.get('posting_deadline'),
                requirements=client_post_info.get('requirements')
            )
            db.session.add(client_post)
            db.session.commit()
            return {"success": True, "client_post_id": client_post.client_post_id}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}

    def update_client_post(self, client_post_id, client_post_info):
        try:
            # 기존 클라이언트 글 업데이트
            client_post = ClientPost.query.filter_by(client_post_id=client_post_id).first()
            if client_post:
                client_post.field_code = client_post_info.get('field_code', client_post.field_code)
                client_post.client_title = client_post_info.get('client_title', client_post.client_title)
                client_post.client_payment_amount = client_post_info.get('client_payment_amount', client_post.client_payment_amount)
                client_post.completion_deadline = client_post_info.get('completion_deadline', client_post.completion_deadline)
                client_post.posting_deadline = client_post_info.get('posting_deadline', client_post.posting_deadline)
                client_post.requirements = client_post_info.get('requirements', client_post.requirements)
                db.session.commit()
                return {"success": True}
            return {"success": False, "message": "클라이언트 글을 찾을 수 없습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}
    
    def save_reference_image(self, reference_image_mapping: ClientPostReferenceImageMapping):
        try:
            db.session.add(reference_image_mapping)
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def delete_reference_image(self, reference_image_mapping: ClientPostReferenceImageMapping):
        try:
            ClientPostReferenceImageMapping.query.filter_by(
                client_post_id=reference_image_mapping.client_post_id,
                reference_image_path=reference_image_mapping.reference_image_path
            ).delete()
            db.session.commit()
            return {'success': True}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def get_reference_image_paths(self, reference_post_id: str) -> list:
        try:
            reference_images = ClientPostReferenceImageMapping.query.filter_by(client_post_id=reference_post_id).all()
            return [image.reference_image_path for image in reference_images]
        except SQLAlchemyError as e:
            return []