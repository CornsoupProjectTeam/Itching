from dataclasses import dataclass, field
from typing import List
from datetime import date
from app.models.client_explore import ClientPostReferenceImageMapping

@dataclass
class ClientExploreDomain:
    client_post_id: str
    client_user_id: str
    field_code: str
    client_title: str
    client_payment_amount: int
    desired_deadline: date
    client_reference_image_mapping: List['ClientPostReferenceImageMapping'] = field(default_factory=list)
