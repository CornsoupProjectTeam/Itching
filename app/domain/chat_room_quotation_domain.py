#chat_room_quotation_domian.py
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Value Objects
# 견적서 상태를 나타내는 Enum 클래스
class EstimateStatus(Enum):
    # 견적서가 작성 중인 상태
    DRAFTING = 'Drafting'
     # 견적서가 검토 중인 상태
    REVIEWING = 'Reviewing'
    # 견적서가 승인된 상태
    APPROVED = 'Approved'

# 견적서 초안의 수를 나타내는 값 객체 (제한 없음)
class DraftCount:
    def __init__(self, count: int):
        if count < 0:
            # 초안 수가 음수일 경우 예외 발생 (음수는 허용하지 않음)
            raise ValueError("Draft count cannot be negative")
        self.count = count  # 초안 수 저장

        
# 중간 점검일과 최종 기한을 관리하는 값 객체
class DateRange:
     # 생성자: 중간 점검일과 최종 기한을 초기화
    def __init__(self, midterm_check: datetime, final_deadline: datetime):
        if final_deadline < midterm_check:
             # 최종 기한이 중간 점검일보다 이전이면 예외 발생
            raise ValueError("Final deadline must be after the midterm check")
        self.midterm_check = midterm_check # 중간 점검일 저장
        self.final_deadline = final_deadline # 최종 기한 저장

# Entity

# 사용자 정보를 관리하는 엔티티
class UserInformation:
    # 생성자: 사용자 ID와 사용자명을 초기화
    def __init__(self, user_id: str, username: str):
        self.user_id = user_id # 사용자 고유 ID
        self.username = username  # 사용자명

# 채팅방 정보를 관리하는 엔티티
class ChatRoom:
    # 생성자: 채팅방 ID와 참여자 목록을 초기화
    def __init__(self, chat_room_id: str, participants: List[UserInformation]):
        self.chat_room_id = chat_room_id # 채팅방 고유 ID
        self.participants = participants # 채팅방 참여자 목록

# Aggregate Root (집합체 루트)
# 채팅방 견적서를 관리하는 집합체 루트 클래스
class ChatRoomQuotation:
    def __init__(
        self, 
        quotation_id: str, 
        chat_room: ChatRoom, 
        client: UserInformation, 
        freelancer: UserInformation, 
        status: EstimateStatus, 
        quotation: float, 
        draft_count: DraftCount, # draft_count: 견적 초안 수 (DraftCount 값 객체)
        date_range: DateRange, #   date_range: 중간 점검일 및 최종 기한 (DateRange 값 객체)
        revision_count: int, #   revision_count: 수정 횟수
        additional_revision_available: bool,  #   additional_revision_available: 추가 수정을 구매할 수 있는지 여부 (True/False)
        commercial_use_allowed: bool, 
        high_resolution_file_available: bool, 
        delivery_route: str
    ):
        self.quotation_id = quotation_id # 견적서 고유 ID
        self.chat_room = chat_room # 채팅방 정보
        self.client = client # 클라이언트 정보
        self.freelancer = freelancer # 프리랜서 정보
        self.status = status # 견적서 상태 (초안 작성 중, 검토 중, 승인됨)
        self.quotation = quotation # 견적 금액
        self.draft_count = draft_count # 초안 수
        self.date_range = date_range # 중간 점검일 및 최종 기한
        self.revision_count = revision_count # 수정 횟수
        self.additional_revision_available = additional_revision_available # 추가 수정 가능 여부
        self.commercial_use_allowed = commercial_use_allowed # 상업적 사용 허용 여부
        self.high_resolution_file_available = high_resolution_file_available # 고해상도 파일 제공 여부
        self.delivery_route = delivery_route # 전달 방식 (예: 이메일, 파일 전송)
        self.created_at = datetime.utcnow() # 견적서 생성 시간 (UTC 기준)
        self.updated_at = datetime.utcnow() # 마지막 업데이트 시간 (UTC 기준)
    
    # 수정 횟수를 업데이트하는 메서드
    # 매개변수:
    #   new_revision_count: 새로운 수정 횟수
    def update_revision_count(self, new_revision_count: int):
        if new_revision_count < 0:
            # 수정 횟수가 음수일 경우 예외 발생
            raise ValueError("Revision count cannot be negative")
        self.revision_count = new_revision_count # 수정 횟수 업데이트
        self.updated_at = datetime.utcnow() # 업데이트 시간 기록
        
    # 견적서 상태를 업데이트하는 메서드
    # 매개변수:
    #   new_status: 새로운 상태 (EstimateStatus Enum을 사용)
    def update_status(self, new_status: EstimateStatus):
        self.status = new_status # 견적서 상태 업데이트
        self.updated_at = datetime.utcnow() # 업데이트 시간 기록

    # 추가 수정 구매 가능 여부를 확인하는 메서드
    # 반환값: 추가 수정 구매 가능 여부 (True/False)
    def can_purchase_additional_revision(self) -> bool:
        return self.additional_revision_available # 추가 수정 가능 여부 반환
