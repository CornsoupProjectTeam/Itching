import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

# Flask 애플리케이션 생성
app = Flask(__name__, static_folder="../frontend/build")

# 루트 디렉터리의 config.py에서 설정 가져오기
app.config.from_object('config.DevelopmentConfig')

CORS(app)

# 데이터베이스 및 MongoDB 초기화
db = SQLAlchemy(app)
mongo = PyMongo(app)

# 환경 변수에서 세션에 사용하는 SECRET_KEY 가져오기
app.secret_key = os.getenv('SECRET_KEY')

# 보안 설정
#app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS 환경에서만 쿠키 전송
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 자바스크립트로 세션 쿠키 접근 금지
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # 크로스 사이트 요청 방지

# 외부 블루프린트 가져오기
from app.blueprints.payments import payments_bp

# 외부 블루프린트 등록
app.register_blueprint(payments_bp, url_prefix='/payments')

# 라우트 초기화 (routes/routes.py에서 초기화)
from app.routes.routes import init_routes
init_routes(app)
