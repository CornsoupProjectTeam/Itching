from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date
from app.models.client_explore import ClientPostReferenceImageMapping

@dataclass
class ClientExploreDomain:
    client_post_id: str
    client_user_id: str
    field_code: Optional[str] = None
    client_title: Optional[str] = None
    client_payment_amount: Optional[int] = None
    completion_deadline: Optional[date] = None
    posting_deadline: Optional[date] = None
    requirements: Optional[str] = None
    client_reference_image_mapping: List[ClientPostReferenceImageMapping] = field(default_factory=list)

    def update_client_post_info(self, client_post_info: dict):
        
        self.field_code = client_post_info.get('field_code', self.field_code)
        self.client_title = client_post_info.get('client_title', self.client_title)
        self.client_payment_amount = client_post_info.get('client_payment_amount', self.client_payment_amount)
        self.completion_deadline = client_post_info.get('completion_deadline', self.completion_deadline)
        self.posting_deadline = client_post_info.get('posting_deadline', self.posting_deadline)
        self.requirements = client_post_info.get('requirements', self.requirements)
    
    def update_reference_image_path(self, new_reference_image: ClientPostReferenceImageMapping):
        # image_path 기준 중복 확인 후 포트폴리오 업데이트
        if not any(client_reference_image.reference_image_path 
                   == new_reference_image.reference_image_path 
                   for client_reference_image in self.client_reference_image_mapping):
            self.client_reference_image_mapping(new_reference_image)
    
    def remove_reference_image_path(self, image_mapping: ClientPostReferenceImageMapping):
        # 주어진 매핑에 해당하는 포트폴리오 이미지를 도메인 객체에서 삭제
        to_remove = [reference_image for reference_image in self.client_reference_image_mapping
                     if reference_image.reference_image_path == image_mapping.reference_image_path]

        for reference_image in to_remove:
            if reference_image in self.client_reference_image_mapping:
                self.client_reference_image_mapping.remove(reference_image)
            else:
                print(f"오류: {reference_image.reference_image_path} 레퍼런스 이미지를 찾을 수 없습니다.")
    