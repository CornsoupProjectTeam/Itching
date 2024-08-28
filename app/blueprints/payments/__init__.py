from flask import Blueprint

# 블루프린트 생성
payments_bp = Blueprint('payments', __name__)

# 라우트 파일 임포트
from . import routes
