#login_repository.py

from app.models.mysql_login import Login
from app.models.mysql_user_consent import UserConsent
from app import db
from app.repositories.user_information_repository import UserInformationRepository

class LoginRepository:
    def __init__(self):
        self.user_info_repository = UserInformationRepository()

    def save(self, user):
        """새로운 사용자를 데이터베이스에 저장합니다."""
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving user: {e}")
            return False
        
    def save_user_consent(self, consent):
        """사용자의 동의 정보를 데이터베이스에 저장합니다."""
        try:
            db.session.add(consent)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving user consent: {e}")
            return False

    def find_by_user_id(self, user_id):
        """사용자 ID로 사용자를 찾습니다."""
        try:
            return Login.query.filter_by(user_id=user_id).first()
        except Exception as e:
            print(f"Error finding user by user_id: {e}")
            return None

    def update(self, user):
        """사용자 정보를 업데이트합니다."""
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return False

    def deactivate_user(self, user_id):
        """사용자를 비활성화 상태로 변경합니다 (탈퇴 처리)."""
        user = self.find_by_user_id(user_id)
        if user:
            user.is_active = False
            return self.update(user)
        else:
            print(f"User with user_id {user_id} not found for deactivation.")
            return False
