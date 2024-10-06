# app/domain/project_list_domain.py

from enum import Enum

class FreelancerBadge(Enum):
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"

class Project:
    def __init__(self, project_id, public_profile_id, field_code, title, payment_amount, avg_response_time, badge, rating, weekend_consultation, weekend_work, created_at, updated_at):
        self.project_id = project_id
        self.public_profile_id = public_profile_id
        self.field_code = field_code
        self.title = title
        self.payment_amount = payment_amount
        self.avg_response_time = avg_response_time
        self.badge = FreelancerBadge(badge)
        self.rating = rating
        self.weekend_consultation = weekend_consultation
        self.weekend_work = weekend_work
        self.created_at = created_at
        self.updated_at = updated_at
