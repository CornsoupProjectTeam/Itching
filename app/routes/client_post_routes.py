# app/routes/client_post_routes.py

from flask import Blueprint, render_template
from app.services.client_post_service import ClientPostService
from app.repositories.client_post_repository import ClientPostRepository

# 블루프린트 설정
client_post_bp = Blueprint('client_post', __name__)

# 레포지토리 및 서비스 초기화
client_post_repository = ClientPostRepository()
client_post_service = ClientPostService(client_post_repository)

@client_post_bp.route('/', methods=['GET'])
def list_client_posts():
    """모든 클라이언트 게시물 목록을 출력"""
    client_posts = client_post_service.get_all_client_posts()
    return render_template('client_post_list.html', client_posts=client_posts)
