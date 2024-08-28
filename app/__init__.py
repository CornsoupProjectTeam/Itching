from flask import Flask
from flask_cors import CORS

# Flask 애플리케이션 생성
app = Flask(__name__, static_folder="../frontend/build")
app.config.from_object('app.config')
CORS(app)

# 여기서 추가 설정 및 블루프린트 등록 등을 수행
from app import routes
from app.blueprints.payments import payments_bp

# 블루프린트 등록
app.register_blueprint(payments_bp, url_prefix='/payments')
