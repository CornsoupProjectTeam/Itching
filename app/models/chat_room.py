from datetime import datetime

class ChatRoom:
    def __init__(self, estimate_id, participants, estimate_status, requirements_mapping,
                 estimate, number_of_drafts, notification_dates, revision_count,
                 additional_revision_purchase_available, commercial_use_allowed,
                 high_resolution_file_available, delivery_method, created_at=None, updated_at=None):
        self.estimate_id = estimate_id
        self.participants = participants
        self.estimate_status = estimate_status
        self.requirements_mapping = requirements_mapping
        self.estimate = estimate
        self.number_of_drafts = number_of_drafts
        self.notification_dates = notification_dates
        self.revision_count = revision_count
        self.additional_revision_purchase_available = additional_revision_purchase_available
        self.commercial_use_allowed = commercial_use_allowed
        self.high_resolution_file_available = high_resolution_file_available
        self.delivery_method = delivery_method
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return self.__dict__
