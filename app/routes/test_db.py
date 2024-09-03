from flask import Blueprint
from app import db, mongo 
from sqlalchemy import text

test_db_bp = Blueprint('test_db', __name__)

@test_db_bp.route('/test_mysql')
def test_mysql():
    try:
        result = db.session.execute(text("SELECT DATABASE();"))
        db_name = result.fetchone()[0]
        return f"MySQL 연결 성공! 데이터베이스 이름: {db_name}"
    except Exception as e:
        return f"MySQL 연결 실패: {e}"

@test_db_bp.route('/test_mongodb')
def test_mongodb():
    try:
        db_names = mongo.cx.list_database_names()
        return f"MongoDB 연결 성공! 데이터베이스 목록: {db_names}"
    except Exception as e:
        return f"MongoDB 연결 실패: {e}"
