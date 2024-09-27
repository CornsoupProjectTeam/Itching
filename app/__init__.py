import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_mail import Mail

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 허용 설정

# UPLOAD_FOLDER 설정
app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(app_dir, 'uploaded_images')

# 루트 디렉터리의 config.py에서 설정 가져오기
app.config.from_object('config.DevelopmentConfig')

CORS(app)

# 데이터베이스 및 MongoDB 초기화
db = SQLAlchemy(app)
mongo = PyMongo(app)
mail = Mail(app)

# 환경 변수에서 세션에 사용하는 SECRET_KEY 가져오기
app.secret_key = os.getenv('SECRET_KEY')

# 보안 설정
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 블루프린트 가져오기 및 등록
from app.blueprints.payments import payments_bp
app.register_blueprint(payments_bp, url_prefix='/payments')

from app.routes.chat_room_list_routes import chat_room_list_bp
app.register_blueprint(chat_room_list_bp, url_prefix='/chatroomlist')

from app.routes.chat_room_routes import chat_room_blueprint
app.register_blueprint(chat_room_blueprint)


# 라우트 초기화
from app.routes.routes import init_routes
init_routes(app)
