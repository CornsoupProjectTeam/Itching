# app/__init__.py
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_cors import CORS
from config import DevelopmentConfig

# .env 파일에서 환경 변수 로드
load_dotenv()

# 확장 모듈 선언 (Flask 앱과 나중에 연결)
db = SQLAlchemy()
mongo = PyMongo()
mail = Mail()
socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')

# Flask 애플리케이션 생성
app = Flask(__name__)

# 설정 적용
app.config.from_object(DevelopmentConfig)

# UPLOAD_FOLDER 설정
app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(app_dir, 'uploaded_images')

# 확장 모듈 초기화 (Flask 앱과 연결)
db.init_app(app)
mongo.init_app(app)
mail.init_app(app)
socketio.init_app(app)

# CORS 설정
CORS(app)

# MongoDB 설정 (mongo_uri와 db_name 사용)
mongo_uri = app.config['MONGO_URI']  # Flask 설정에서 Mongo URI 가져오기
db_name = 'itching_mongodb'
from app.models.mongo_message import MongoMessage  # MongoMessage 클래스 임포트
mongo_message = MongoMessage(mongo_uri, db_name)  # MongoMessage 인스턴스 초기화

# 보안 설정
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 라우트 및 블루프린트 등록
from app.routes.routes import init_routes
init_routes(app)

from app.blueprints.payments import payments_bp
app.register_blueprint(payments_bp, url_prefix='/payments')
