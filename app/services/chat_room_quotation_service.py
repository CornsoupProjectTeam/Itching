#app/services/chat_room_quotation_service.py
import uuid
from datetime import datetime
from app import db
from app.models.chat_room_quotation import ChatRoomQuotation
from sqlalchemy.exc import SQLAlchemyError

class QuotationService:
    """
    견적서 관련 비즈니스 로직을 처리하는 서비스 레이어
    """

    @staticmethod
    def create_quotation(data: dict) -> dict:
        """
        견적서 생성을 위한 비즈니스 로직 처리
        :param data: 견적서 생성을 위한 폼 데이터
        :return: 생성된 견적서 데이터 또는 오류 메시지
        """
        try:
            # UUID 생성: quotation_id가 없으면 UUID를 생성
            quotation_id = data.get('quotation_id') or str(uuid.uuid4())

            # 클라이언트 요구사항, 견적 금액 등 필수 데이터 처리
            client_requirements = data.get('client_requirements')
            quotation = float(data.get('quotation', 0))  # 견적 금액
            number_of_drafts = int(data.get('number_of_drafts'))  # 초안 개수
            final_deadline = data.get('final_deadline')
            midterm_check = data.get('midterm_check')
            revision_count = int(data.get('revision_count'))  # 수정 개수
            additional_revision_available = 'additional_revision_available' in data
            commercial_use_allowed = 'commercial_use_allowed' in data
            high_resolution_file_available = 'high_resolution_file_available' in data
            delivery_route = data.get('delivery_route')

            # 반환할 JSON 데이터 구조
            quotation_data = {
                "client_requirements": client_requirements,
                "quotation_id": quotation_id,
                "quotation": quotation,
                "number_of_drafts": number_of_drafts,
                "final_deadline": final_deadline,
                "midterm_check": midterm_check,
                "revision_count": revision_count,
                "additional_revision_available": additional_revision_available,
                "commercial_use_allowed": commercial_use_allowed,
                "high_resolution_file_available": high_resolution_file_available,
                "delivery_route": delivery_route
            }

            return {"success": True, "data": quotation_data}
        
        except ValueError as e:
            # 데이터 변환 과정에서 발생하는 ValueError 처리
            return {"success": False, "error": f"Invalid data: {str(e)}"}
        
        except Exception as e:
            # 기타 예외 처리
            return {"success": False, "error": str(e)}

    @staticmethod
    def save_quotation(data: dict) -> dict:
        """
        견적서 저장을 위한 비즈니스 로직 처리
        :param data: 폼 데이터
        :return: 저장된 견적서 또는 오류 메시지
        """
        try:
            # 데이터베이스에 저장할 견적서 생성
            new_quotation = ChatRoomQuotation(
                quotation_id=data.get('quotation_id') or str(uuid.uuid4()),
                chat_room_id=data.get('chat_room_id'),
                client_user_id=data.get('client_user_id'),
                freelancer_user_id=data.get('freelancer_user_id'),
                quotation_st=data.get('quotation_st', 'Submitted'),
                quotation=float(data.get('quotation', 0)),
                number_of_drafts=int(data.get('number_of_drafts', 0)),
                midterm_check=datetime.strptime(data.get('midterm_check', '2024-01-01'), '%Y-%m-%d'),
                final_deadline=datetime.strptime(data.get('final_deadline', '2024-01-01'), '%Y-%m-%d'),
                revision_count=int(data.get('revision_count', 0)),
                additional_revision_purchase_available='additional_revision_available' in data,
                commercial_use_allowed='commercial_use_allowed' in data,
                high_resolution_file_available='high_resolution_file_available' in data,
                delivery_route=data.get('delivery_route'),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # 데이터베이스에 저장
            db.session.add(new_quotation)
            db.session.commit()

            # 저장 성공 시 반환 데이터
            return {"success": True, "quotation_id": new_quotation.quotation_id}

        except SQLAlchemyError as e:
            # 데이터베이스 에러 처리
            db.session.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}

        except ValueError as e:
            # 데이터 변환 에러 처리
            db.session.rollback()
            return {"success": False, "error": f"Invalid data: {str(e)}"}

        except Exception as e:
            # 기타 예외 처리
            db.session.rollback()
            return {"success": False, "error": str(e)}
        
class QuotationService:
    """
    견적서 관련 비즈니스 로직을 처리하는 서비스 레이어
    """

    @staticmethod
    def update_quotation(quotation_id: str, data: dict) -> dict:
        """
        견적서 수정을 위한 비즈니스 로직 처리
        :param quotation_id: 수정할 견적서의 ID
        :param data: 견적서 수정을 위한 폼 데이터
        :return: 수정된 견적서 데이터 또는 오류 메시지
        """
        try:
            # 기존 견적서 조회
            quotation = ChatRoomQuotation.query.filter_by(quotation_id=quotation_id).first()

            if not quotation:
                return {"success": False, "error": "Quotation not found"}

            # 폼 데이터 처리
            quotation.chat_room_id = data.get('chat_room_id').strip()
            quotation.client_user_id = data.get('client_user_id').strip()
            quotation.freelancer_user_id = data.get('freelancer_user_id').strip()
            quotation.quotation_st = data.get('quotation_st', 'Submitted').strip()
            quotation.quotation = float(data.get('quotation', 0))
            quotation.number_of_drafts = int(data.get('number_of_drafts', 0))
            quotation.midterm_check = datetime.strptime(data.get('midterm_check', '2024-01-01').strip(), '%Y-%m-%d')
            quotation.final_deadline = datetime.strptime(data.get('final_deadline', '2024-01-01').strip(), '%Y-%m-%d')
            quotation.revision_count = int(data.get('revision_count', 0))
            quotation.additional_revision_purchase_available = 'additional_revision_available' in data
            quotation.commercial_use_allowed = 'commercial_use_allowed' in data
            quotation.high_resolution_file_available = 'high_resolution_file_available' in data
            quotation.delivery_route = data.get('delivery_route').strip()
            quotation.updated_at = datetime.utcnow()

            # 데이터베이스에 저장
            db.session.commit()

            return {"success": True, "quotation_id": quotation.quotation_id}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}

        except ValueError as e:
            db.session.rollback()
            return {"success": False, "error": f"Invalid data: {str(e)}"}

        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

