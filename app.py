from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_pymongo import PyMongo
from flask_cors import CORS

# Flask 애플리케이션 생성
app = Flask(__name__, static_folder="../frontend/build")
app.config.from_object('app.config')  # 애플리케이션 설정 로드

# 데이터베이스 및 MongoDB 초기화 (현재 주석 처리됨)
# db = SQLAlchemy(app)
# mongo = PyMongo(app)

# CORS 설정
CORS(app)

# 기본 API 라우트 불러오기
from app import routes  

# 결제 블루프린트 등록
from app.blueprints.payments import payments_bp
app.register_blueprint(payments_bp, url_prefix='/payments')
