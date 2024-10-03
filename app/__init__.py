#app/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_migrate import Migrate


app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# UPLOAD_FOLDER 설정
app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(app_dir, 'uploaded_images')

# 루트 디렉터리의 config.py에서 설정 가져오기
app.config.from_object('config.DevelopmentConfig')

CORS(app)

db = SQLAlchemy(app)
mongo = PyMongo(app)
mail = Mail(app)

# 환경 변수에서 세션에 사용하는 SECRET_KEY 가져오기
app.secret_key = os.getenv('SECRET_KEY')

# 보안 설정
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Flask-Migrate 초기화
migrate = Migrate(app, db)

# 블루프린트 가져오기 및 등록
from app.blueprints.payments import payments_bp
app.register_blueprint(payments_bp, url_prefix='/payments')

# from app.routes.chat_room_list_routes import chat_room_list_bp
# app.register_blueprint(chat_room_list_bp, url_prefix='/chatroomlist')

# 블루프린트 가져오기 및 등록
from app.routes.chat_room_routes import chat_room_bp  # chat_room_bp로 변경
app.register_blueprint(chat_room_bp, url_prefix='/chatroom')

from app.routes.chat_room_quotation_routes import quotation_bp
app.register_blueprint(quotation_bp, url_prefix='/chatroom/quotation')

# Blueprint 등록
from app.routes.project_list_routes import project_list_bp
app.register_blueprint(project_list_bp, url_prefix='/projectlist')


# 모델을 하단에서 임포트
from app.models import project_info, project_list
# 모델 임포트
from app.models.chat_room_master import ChatRoomMaster
from app.models.chat_room_quotation import ChatRoomQuotation
from app.models.user_information import UserInformation


# 라우트 초기화
from app.routes.routes import init_routes
init_routes(app)
