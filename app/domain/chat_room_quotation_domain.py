#chat_room_quotation_domian.py
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Value Objects

class EstimateStatus(Enum):
    DRAFTING = 'Drafting'
    REVIEWING = 'Reviewing'
    APPROVED = 'Approved'

class DraftCount:
    def __init__(self, count: int):
        if count < 1 or count > 5:
            raise ValueError("Draft count must be between 1 and 5")
        self.count = count

class DateRange:
    def __init__(self, midterm_check: datetime, final_deadline: datetime):
        if final_deadline < midterm_check:
            raise ValueError("Final deadline must be after the midterm check")
        self.midterm_check = midterm_check
        self.final_deadline = final_deadline

# Entity
class UserInformation:
    def __init__(self, user_id: str, username: str):
        self.user_id = user_id
        self.username = username

class ChatRoom:
    def __init__(self, chat_room_id: str, participants: List[UserInformation]):
        self.chat_room_id = chat_room_id
        self.participants = participants

# Aggregate Root
class ChatRoomQuotation:
    def __init__(
        self, 
        quotation_id: str, 
        chat_room: ChatRoom, 
        client: UserInformation, 
        freelancer: UserInformation, 
        status: EstimateStatus, 
        quotation: float, 
        draft_count: DraftCount, 
        date_range: DateRange, 
        revision_count: int, 
        additional_revision_available: bool, 
        commercial_use_allowed: bool, 
        high_resolution_file_available: bool, 
        delivery_route: str
    ):
        self.quotation_id = quotation_id
        self.chat_room = chat_room
        self.client = client
        self.freelancer = freelancer
        self.status = status
        self.quotation = quotation
        self.draft_count = draft_count
        self.date_range = date_range
        self.revision_count = revision_count
        self.additional_revision_available = additional_revision_available
        self.commercial_use_allowed = commercial_use_allowed
        self.high_resolution_file_available = high_resolution_file_available
        self.delivery_route = delivery_route
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def update_revision_count(self, new_revision_count: int):
        if new_revision_count < 0:
            raise ValueError("Revision count cannot be negative")
        self.revision_count = new_revision_count
        self.updated_at = datetime.utcnow()
    
    def update_status(self, new_status: EstimateStatus):
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def can_purchase_additional_revision(self) -> bool:
        return self.additional_revision_available
