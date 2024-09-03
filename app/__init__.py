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

# 블루프린트가져오기
from app.blueprints.payments import payments_bp

# 블루프린트 등록
app.register_blueprint(payments_bp, url_prefix='/payments')

# 라우트 초기화
from app.routes.routes import init_routes
init_routes(app)