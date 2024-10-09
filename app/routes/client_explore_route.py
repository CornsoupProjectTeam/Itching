from flask import Blueprint, request, jsonify, g
from app.services.client_explore_service import ClientExploreService
from app.repositories.client_explore_repository import ClientExploreRepository
from app.services.post_management_service import PostManagementService  # PostManagementService 임포트 추가

client_explore_bp = Blueprint('client_explore', __name__, url_prefix='/client-explore')

@client_explore_bp.before_request
def before_request():
    # 요청에서 client_post_id 가져오기
    client_post_id = request.view_args.get('client_post_id')

    # 리포지토리와 서비스 객체 초기화 시 client_post_id를 전달하여 초기화
    g.client_explore_repository = ClientExploreRepository()
    g.post_management_service = PostManagementService()  # PostManagementService 객체 초기화
    g.client_explore_service = ClientExploreService(g.client_explore_repository, g.post_management_service, client_post_id)

@client_explore_bp.route('/details/<client_post_id>', methods=['GET'])
def get_client_post_information(client_post_id):
    try:
        # 서비스 계층을 통해 클라이언트 글 정보를 가져옴
        client_post_info = g.client_explore_service.get_client_post_information()

        return jsonify(client_post_info), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 404

@client_explore_bp.route('/client-post/<client_post_id>', methods=['POST', 'PUT'])
def create_or_update_client_post(client_post_id):
    try:
        # 프론트엔드에서 전달된 데이터 받아오기
        client_post_info = {
            'field_code': request.json.get('field_code'),
            'client_title': request.json.get('client_title'),
            'client_payment_amount': request.json.get('client_payment_amount'),
            'completion_deadline': request.json.get('completion_deadline'),
            'posting_deadline': request.json.get('posting_deadline'),
            'requirements': request.json.get('requirements')
        }
        
        # 이미지와 삭제할 이미지 리스트 가져오기
        portfolio_images = request.files.getlist('portfolio_images')
        deleted_portfolio_image_paths = request.json.get('deleted_portfolio_image_paths', [])

        # POST 요청: 새로운 클라이언트 포스트 생성
        if request.method == 'POST':
            result = g.client_explore_service.create_client_post(client_post_info, client_post_id)
            if not result['success']:
                return jsonify(result), 400
        
        # PUT 요청: 기존 클라이언트 포스트 업데이트
        elif request.method == 'PUT':
            result = g.client_explore_service.update_client_post(client_post_info, client_post_id)
            if not result['success']:
                return jsonify(result), 400
        
        # 레퍼런스 이미지 업데이트 처리 (포트폴리오 이미지나 삭제할 이미지가 있을 때만)
        if portfolio_images or deleted_portfolio_image_paths:
            image_result = g.client_explore_service.update_reference_images(portfolio_images, deleted_portfolio_image_paths)
            if not image_result['success']:
                return jsonify(image_result), 400

        return jsonify({'success': True, 'message': '클라이언트 포스트가 성공적으로 처리되었습니다.'}), 200

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'서버 오류: {str(e)}'}), 500