import os
from dotenv import load_dotenv
from mongoengine import connect

# .env 파일 로드
load_dotenv()

class Config:
    # MySQL 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB 설정
    MONGO_URI = os.getenv('MONGO_URI')
    connect(host=MONGO_URI, alias='default')

    # Flask Secret Key (세션 관리, CSRF 방지 등)
    # SECRET_KEY = os.getenv('SECRET_KEY')

# 개발 환경을 위한 추가 설정
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # SQLAlchemy가 실행하는 SQL 쿼리를 출력

# 프로덕션 환경을 위한 추가 설정
# class ProductionConfig(Config):
#     DEBUG = False

# 현재 환경 설정을 선택
config = {
    'development': DevelopmentConfig,
    # 'production': ProductionConfig,
}
