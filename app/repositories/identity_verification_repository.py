# repository/identity_verification_repository.py

from app.models.identity_verification import db, IdentityVerification
from datetime import datetime

class IdentityVerificationRepository:
    def save_verification(self, phone_number, verification_code, expiration_time):
        verification = IdentityVerification(
            user_id=None,  # 적절한 user_id 설정 필요
            phone_number=phone_number,
            verification_status=False,
            verification_code=verification_code,
            expiration_time=expiration_time
        )
        db.session.add(verification)
        db.session.commit()

    def get_verification_by_phone(self, phone_number):
        return IdentityVerification.query.filter_by(phone_number=phone_number).first()

    def update_verification_status(self, user_id, phone_number, status):
        verification = IdentityVerification.query.filter_by(phone_number=phone_number).first()
        if verification:
            verification.verification_status = status
            verification.user_id = user_id
            verification.updated_at = datetime.utcnow()
            db.session.commit()
