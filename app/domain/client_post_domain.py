# app/domain/client_post_domain.py

from datetime import datetime

class ClientPost:
    def __init__(self, client_post_id, client_user_id, field_code, title, payment_amount, desired_deadline, created_at, updated_at):
        self.client_post_id = client_post_id  # 게시물 ID
        self.client_user_id = client_user_id  # 클라이언트 ID
        self.field_code = field_code          # 분야 코드
        self.title = title                    # 게시물 제목
        self.payment_amount = payment_amount  # 결제 금액
        self.desired_deadline = desired_deadline  # 희망 마감일
        self.created_at = created_at          # 게시물 생성일
        self.updated_at = updated_at          # 게시물 수정일

    # 게시물 정보를 업데이트하는 메서드
    def update_post(self, title, payment_amount, desired_deadline):
        self.title = title
        self.payment_amount = payment_amount
        self.desired_deadline = desired_deadline
        self.updated_at = datetime.utcnow()
