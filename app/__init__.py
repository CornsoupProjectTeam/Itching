#app/__init__.py
import os
from flask import Flask
from config import DevelopmentConfig
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_mail import Mail

app = Flask(__name__)

# 설정을 Flask 애플리케이션에 적용
app.config.from_object(DevelopmentConfig)

# Flask-SocketIO 초기화
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# UPLOAD_FOLDER 설정
app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(app_dir, 'uploaded_images')

# CORS 설정
CORS(app)

# 확장 모듈 초기화
db = SQLAlchemy(app)
mongo = PyMongo(app)
mail = Mail(app)

# 보안 설정
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 라우트 및 블루프린트 임포트 후 등록
from app.routes.routes import init_routes
init_routes(app)

#app/routes/routes.py에서 등록할 것
from app.routes.chat_room_routes import chat_room_bp
app.register_blueprint(chat_room_bp, url_prefix='/chatroom')

from app.routes.chat_room_quotation_routes import quotation_bp
app.register_blueprint(quotation_bp, url_prefix='/chatroom/quotation')

from app.blueprints.payments import payments_bp
app.register_blueprint(payments_bp, url_prefix='/payments')

from app.routes.image_upload import image_upload_bp
app.register_blueprint(image_upload_bp)
