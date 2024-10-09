from flask import session
from datetime import datetime, timedelta
import pytz
from app.domain.client_explore_domain import ClientExploreDomain
from app.utils.id_generator import generate_client_post_id, generate_post_id
from app.utils.image_upload import upload_image, delete_image
from app.models.client_explore import ClientPostReferenceImageMapping
from app.services.post_management_service import PostManagementService

class ClientExploreService:
    def __init__(self, client_explore_repository, post_management_service,
                 client_post_id=None):
        self.client_explore_repository = client_explore_repository
        self.domain = self.initialize_domain(client_post_id)
        self.post_management_service = post_management_service

    def initialize_domain(self, client_post_id: str = None):
        if client_post_id:
            # 기존 데이터를 조회하여 도메인 객체 초기화
            client_post_info = self.client_explore_repository.get_client_post_information(client_post_id)
            
            if client_post_info:
                # 도메인 객체에 데이터를 설정
                self.domain = ClientExploreDomain(
                    client_post_id=client_post_info.client_post_id,
                    client_user_id=client_post_info.client_user_id,
                    field_code=client_post_info.field_code,
                    client_title=client_post_info.client_title,
                    client_payment_amount=client_post_info.client_payment_amount,
                    completion_deadline=client_post_info.completion_deadline,
                    posting_deadline=client_post_info.posting_deadline,
                    requirements=client_post_info.requirements,
                    client_reference_image_mapping=client_post_info.client_reference_image_mapping  # 그대로 설정
                )
            else:
                raise ValueError("클라이언트 글 정보를 찾을 수 없습니다.")
        else:
            # POST 요청에서 새로운 도메인 객체를 초기화할 때
            self.domain = ClientExploreDomain(
                client_post_id=generate_client_post_id(),
                client_user_id=session.get('user_id'),
                field_code=None,
                client_title=None,
                client_payment_amount=0,
                completion_deadline=None,
                posting_deadline=None,
                requirements=None,
                client_reference_image_mapping=[]
            )

        return self.domain
    
    def get_client_post_information(self) -> dict:
        client_post = self.domain

        if client_post is None:
            raise ValueError("도메인 객체가 초기화되지 않았습니다.")

        return {
            "client_post_id": client_post.client_post_id,
            "client_user_id": client_post.client_user_id,
            "field_code": client_post.field_code,
            "client_title": client_post.client_title,
            "client_payment_amount": client_post.client_payment_amount,
            "completion_deadline": client_post.completion_deadline.isoformat() if client_post.completion_deadline else None,
            "posting_deadline": client_post.posting_deadline.isoformat() if client_post.posting_deadline else None,
            "requirements": client_post.requirements,
            "client_reference_image_mapping": [
                {
                    "client_post_id": image.client_post_id,
                    "reference_image_path": image.reference_image_path
                } for image in client_post.client_reference_image_mapping
            ]
        }

    def get_filtered_and_sorted_client_posts(self, min_price, max_price, within_weeks, sort_field, order, user_id=None, field_code=None):
        # 한국 시간대 설정
        KST = pytz.timezone('Asia/Seoul')

        # 현재 시간을 한국 시간대로 변환하고 희망 제작마감일 계산
        deadline_date = datetime.now(KST) + timedelta(weeks=within_weeks) if within_weeks else None

        # 필터링 조건이 있는 경우에만 필터링 수행
        if min_price is not None or max_price is not None or deadline_date is not None or field_code is not None:
            filtered_client_posts = self.client_explore_repository.filter_client_posts(min_price, max_price, deadline_date, field_code)
        else:
            # 필터링 조건이 없으면 모든 클라이언트 데이터 가져오기
            filtered_client_posts = self.client_explore_repository.get_all_client_posts()

        # 추천순 정렬인 경우 외부 추천 서비스 호출
        #if sort_field == 'recommendation' and user_id is not None:
        #    return self.recommendation_service.get_recommendations(filtered_client_posts, user_id)
        #else:
        
        # 일반 정렬 수행 (마감기한순 또는 신규등록순)
        return self.client_explore_repository.sort_client_posts(filtered_client_posts, sort_field, order)

    def create_client_post(self, client_post_info, client_post_id):
        # 도메인 객체가 초기화되지 않은 경우 에러 반환
        if not self.domain or not self.domain.client_post_id:
            raise ValueError("도메인 객체가 초기화되지 않았습니다. client_post_id가 필요합니다.")

        # 레포지토리 계층에서 새로운 행 생성 및 값 저장
        result = self.client_explore_repository.create_client_post(self.domain.client_post_id, self.domain.client_user_id, client_post_info)

        if result['success']:
            # 도메인 객체 업데이트
            self.initialize_domain(result['client_post_id'])
            self.update_post_management()

        return result

    def update_client_post(self, client_post_info, client_post_id):
        # 도메인 객체가 초기화되지 않은 경우 에러 반환
        if not self.domain or not self.domain.client_post_id:
            raise ValueError("도메인 객체가 초기화되지 않았습니다. client_post_id가 필요합니다.")

        # 레포지토리 계층에 클라이언트 글 업데이트 요청
        result = self.client_explore_repository.update_client_post(self.domain.client_post_id, client_post_info)
        if result['success']:
            # 도메인 객체 업데이트
            self.domain.update_client_post_info(client_post_info)
            self.update_post_management()
        return result
    
    def update_reference_images(self, reference_images: list, deleted_reference_image_paths: list):        
        # 1. 삭제된 레퍼런스 이미지 처리
        if deleted_reference_image_paths:
            for image_path in deleted_reference_image_paths:
                reference_image_mapping = ClientPostReferenceImageMapping(
                    client_post_id=self.domain.client_post_id,
                    reference_image_path=image_path
                )
                result = self.client_explore_repository.delete_reference_image(reference_image_mapping)
                if not result['success']:
                    return {"success": False, "message": f'{image_path} 레퍼런스 이미지 삭제에 실패했습니다.'}

                # 이미지 파일도 실제로 삭제
                delete_image(self.domain.client_user_id, image_path)

                self.domain.remove_reference_image_path(reference_image_mapping)

            # 삭제 작업이 성공적으로 수행되었을 때 메시지 반환
            return {'success': True, 'message': '레퍼런스 이미지가 성공적으로 삭제되었습니다.'}

        # 2. 새로운 레퍼런스 이미지 업로드 처리
        uploaded_image_paths = []    

        if reference_images:
            for file in reference_images:
                filename, error = upload_image(file, self.domain.client_user_id)

                if error:
                    # 하나라도 업로드에 실패하면 이미 업로드된 파일들 삭제 후 반환
                    for uploaded_file in uploaded_image_paths:
                        delete_image(self.domain.client_user_id, uploaded_file)  # 업로드된 이미지 삭제

                    return {"success": False, "message": f'{file.filename} 업로드에 실패했습니다. 에러: {error}'}

                # 업로드 성공 시 파일 경로 저장
                uploaded_image_paths.append(filename)

            # 모든 이미지가 성공적으로 업로드되었을 때
            for filename in uploaded_image_paths:
                reference_image_mapping = ClientPostReferenceImageMapping(
                    client_post_id=self.domain.client_post_id,
                    reference_image_path=image_path
                )
                result = self.repository.save_reference_image(reference_image_mapping)

                if not result['success']:
                    # DB 저장 중 문제가 발생하면 업로드된 파일들 삭제 후 반환
                    for uploaded_file in uploaded_image_paths:
                        delete_image(self.domain.client_user_id, uploaded_image_paths)

                    return {'success': False, 'message': f'{filename} 레퍼런스 이미지 저장에 실패했습니다.'}

            # 모든 레퍼런스 이미지가 성공적으로 DB에 저장된 경우에만 도메인 객체 업데이트
            if uploaded_image_paths:
                
                self.domain.update_reference_image_path(reference_image_mapping)
                return {'success': True, 'message': '레퍼런스 이미지가 성공적으로 업데이트되었습니다.'}
        
        # 만약 reference_images와 deleted_reference_image_paths 모두 없으면 에러 메시지 반환
        return {'success': False, 'message': '레퍼런스 이미지나 삭제할 레퍼런스 이미지가 제공되지 않았습니다.'}

    def update_post_management(self):
        user_id = self.domain.client_user_id
        category = 'Client'
        reference_post_id = self.domain.client_post_id
        project_title = self.domain.client_title

        result = self.post_management_service.update_post_management(user_id, category, reference_post_id, project_title)
        
        if not result['success']:                   
            raise ValueError("글관리에 클라이언트 글 정보를 저장할 수 없습니다.")
    
    def deleted_reference_images_for_post_management(self, reference_post_id: str):
        # 빈 리스트와 반환된 이미지 경로 리스트를 정리하여 update_reference_images 호출
        reference_images = []
        deleted_reference_image_paths = self.repository.get_reference_image_paths(reference_post_id)
        update_result = self.update_reference_images(reference_images, deleted_reference_image_paths)

        if not update_result['success']:
            raise ValueError("이미지 삭제에 실패했습니다.")

        return update_result