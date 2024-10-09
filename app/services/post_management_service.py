from app.models.post_management import PostManagement
from app.utils.id_generator import generate_post_id

class PostManagementService:
    def __init__(self, postmanagement_repository, client_explore_service):
        self.repository = postmanagement_repository
        self.client_explore_service = client_explore_service
    
    def get_posts_by_user_id(self, user_id: str) -> dict:
        posts = self.repository.get_posts_by_user_id(user_id)
        if posts is not None:
            # PostManagement 객체들을 dict 형태로 변환
            posts_list = [{'post_id': post.post_id, 'user_id': post.user_id, 'category': post.category,
                           'reference_post_id': post.reference_post_id, 'project_title': post.project_title,
                           'updated_at': post.updated_at} for post in posts]
            return {'success': True, 'posts': posts_list}
        else:
            raise ValueError("사용자의 작성글 목록이 없습니다.")

    def update_post_management(self, user_id, category, reference_post_id, project_title):
        new_post = PostManagement(
            post_id = generate_post_id(),
            user_id = user_id,
            category = category,
            reference_post_id = reference_post_id,
            project_title = project_title
        )

        result = self.repository.save_post_management(new_post)
        
        if result['success']:
            return result
        else:
            raise ValueError("작성글관리에 글 정보를 저장할 수 없습니다.")

    def delete_post_management(self, post_id: str) -> dict:
        # post_id가 PST로 시작하는지 확인
        if post_id.startswith('PST'):
            # post_id를 기반으로 reference_post_id를 가져옴
            reference_post_id = self.repository.get_reference_post_id_by_post_id(post_id)
            
            if reference_post_id:
                # reference_post_id를 deleted_reference_images_for_post_management에 전달하고 결과 확인
                update_result = self.client_explore_service.deleted_reference_images_for_post_management(reference_post_id)

                if not update_result['success']:
                    raise ValueError("관련 레퍼런스 이미지 삭제에 실패하여 작성글 관리에서 글 정보를 삭제할 수 없습니다.")

        # 레퍼런스 이미지 삭제가 성공했거나 해당 로직이 실행되지 않은 경우에만 글 정보 삭제
        result = self.repository.delete_post_management(post_id)
        
        if result['success']:
            return {'success': True, 'meaasge':"작성글관리에서 해당 글 정보를 삭제했습니다."}
        else:
            raise ValueError(result['message'])
