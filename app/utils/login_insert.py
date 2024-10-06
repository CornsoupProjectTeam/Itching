from flask import Flask
from app.models.login import Login, db
from app.utils.encryption_util import EncryptionUtils

# Flask 애플리케이션 생성 및 설정 불러오기
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# SQLAlchemy 초기화
db.init_app(app)

def insert_login_data(user_id, provider_id, password):
    # 암호화된 패스워드 생성
    encrypted_password = EncryptionUtils.hash_password(password)

    # 새로운 Login 객체 생성
    new_login = Login(
        user_id=user_id,
        provider_id=provider_id,
        password=encrypted_password        
    )

    # 데이터베이스에 삽입
    db.session.add(new_login)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():  # Flask 앱 컨텍스트 내에서 실행
        # 예시 데이터
        user_id = 'ujin0628'
        provider_id = 'local'
        password = '12345'

        # 데이터 삽입 함수 호출
        insert_login_data(user_id, provider_id, password)
