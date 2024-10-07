from flask import current_app
import os
from app.domain.freelancer_information_domain import *
from app.models.freelancer_information import (
    PreferredWorkStyleMapping,
    Review
)
from app.utils.encryption_util import EncryptionUtils

class FreelancerInformationService:
    def __init__(self, freelancer_information_repository,
                 freelancer_registration_service,
                 freelancer_user_id):
        self.repository = freelancer_information_repository
        self.freelancer_registration_service = freelancer_registration_service
        self.freelancer_user_id = freelancer_user_id
        
        result = self.repository.get_public_profile_id(self.freelancer_user_id)
        if result['success']:
            self.public_profile_id = result['public_profile_id']
        else: 
            return result

        self.domain = self.initialize_domain()

    def initialize_domain(self):

        profile_data = self.repository.get_public_profile_for_freelancer_information(self.public_profile_id)
        
        if not profile_data['success']:
            return ValueError('공개 프로필을 가져오는데 실패하였습니다.')

        # 프로필과 맵핑 데이터가 있는 경우 도메인 객체 초기화
        public_profile = profile_data['profile']
        service_options = profile_data.get('service_options', [])
        price_range = profile_data.get('price_range', [])
        preferred_work_style = profile_data.get('preferred_work_style', [])
        account_info = profile_data.get('account_info', [])
        review = profile_data.get('review', [])
        review_summary = profile_data.get('review_summary', [])

        # 도메인 객체에 데이터를 설정
        self.domain = FreelancerInformationDomain(
            freelancer_badge=public_profile.freelancer_badge,
            match_count=public_profile.match_count,
            freelancer_intro_one_liner=public_profile.freelancer_intro_one_liner,
            project_duration=public_profile.project_duration,
            public_profile_registration_st=public_profile.public_profile_registration_st,
            service_options=service_options,
            price_range=price_range,
            preferred_work_style=preferred_work_style,
            account_info=account_info,
            review=review,
            review_summary=review_summary
        )

        return self.domain

    # 프리랜서 정보 조회
    def get_freelancer_information(self):
        profile = self.domain

        # 도메인 객체에서 필요한 데이터 추출 및 반환
        if profile:
            return {
                "freelancer_badge": profile.freelancer_badge,
                "match_count": profile.match_count,
                "freelancer_intro_one_liner": profile.freelancer_intro_one_liner,
                "project_duration": profile.project_duration,
                "public_profile_registration_st": profile.public_profile_registration_st,
                "service_options": {
                    "weekend_consultation": profile.service_options.weekend_consultation,
                    "weekend_work": profile.service_options.weekend_work
                } if profile.service_options else None,
                "price_range": {
                    "min_price": profile.price_range.min_price,
                    "max_price": profile.price_range.max_price,
                    "price_unit": profile.price_range.price_unit
                } if profile.price_range else None,
                "preferred_work_style": [
                    {
                        "preferred_code": style.preferred_code,
                    } for style in profile.preferred_work_style
                ] if profile.preferred_work_style else None,
                "account_info": {
                    "bank_name": profile.account_info.bank_name,
                    "account_number": profile.account_info.account_number,
                    "account_holder": profile.account_info.account_holder,
                    "account_type": profile.account_info.account_type
                } if profile.account_info else None,
                "review": [
                    {
                        "sequence": review.sequence,
                        "public_profile_id": review.public_profile_id,
                        "review_title": review.review_title,
                        "review_text": review.review_text,
                        "rating": review.rating,
                        "created_at": review.created_at,
                        "updated_at": review.updated_at,
                        "client_user_id": review.client_user_id
                    } for review in profile.review
                ] if profile.review else None,
                "review_summary": {
                    "total_reviews": profile.review_summary.total_reviews,
                    "average_rating": profile.review_summary.average_rating
                } if profile.review_summary else None
            }
        else:
            return None
    
    # PublicProfileList 가져오기
    def get_public_profile_list(self, public_profile_id: str):
        result = self.repository.get_public_profile_list(public_profile_id)
        
        if result['success']:
            profile_list = result['profile_list']            
            return {
                "success": True,
                "data": {
                    "public_profile_id": profile_list.public_profile_id,
                    "nickname": profile_list.nickname,
                    "profile_image_path": profile_list.profile_image_path,
                    "freelancer_badge": profile_list.freelancer_badge,
                    "match_count": profile_list.match_count,
                    "freelancer_registration_date": profile_list.freelancer_registration_date,
                    "average_rating": profile_list.average_rating,
                    "created_at": profile_list.created_at,
                    "updated_at": profile_list.updated_at
                }
            }
        else:
            return {
                "success": False,
                "message": result['message']
            }

    # 프로젝트 기간 업데이트
    def update_project_duration(self, project_duration):
        result = self.repository.save_project_duration(self.public_profile_id, project_duration)
        
        if result['success']:            
            self.domain.update_project_duration(project_duration)
            return {'success': True, 'message': '프로젝트 기간이 성공적으로 저장되었습니다.'}
        
        print(f"프로젝트 기간 저장 실패: result={result}")
        return {'success': False, 'message': '프로젝트 기간 저장에 실패했습니다.'}

    # 공개 프로필 등록 상태 업데이트
    def update_public_profile_registration_st(self, registration_status):
        result = self.repository.save_public_profile_registration_st(self.public_profile_id, registration_status)
        
        if result['success']:            
            self.domain.update_public_profile_registration_st(registration_status)
            return {'success': True, 'message': '등록 상태가 성공적으로 저장되었습니다.'}
        
        return {'success': False, 'message': '등록 상태 저장에 실패했습니다.'}

    # 프리랜서 소개 한 줄 업데이트
    def update_freelancer_intro_one_liner(self, intro_one_liner):
        result = self.repository.save_freelancer_intro_one_liner(self.public_profile_id, intro_one_liner)
        
        if result['success']:            
            self.domain.update_freelancer_intro_one_liner(intro_one_liner)
            return {'success': True, 'message': '프리랜서 소개가 성공적으로 저장되었습니다.'}
        
        print(f"프리랜서 소개 한 줄 업데이트 실패: result={result}")
        return {'success': False, 'message': '프리랜서 소개 저장에 실패했습니다.'}

    # 서비스 옵션 업데이트
    def update_serviceoptions(self, weekend_consultation, weekend_work):
        result = self.repository.save_serviceoptions(self.public_profile_id, weekend_consultation, weekend_work)
        if result['success']:
            self.domain.update_service_options(weekend_consultation, weekend_work)
            return {'success': True, 'message': '서비스 옵션이 성공적으로 저장되었습니다.'}
        
        print(f"서비스 옵션 업데이트 실패: result={result}")
        return {'success': False, 'message': '서비스 옵션 저장에 실패했습니다.'}

    # 가격 범위 업데이트
    def update_price_range(self, min_price, max_price, price_unit):
        result = self.repository.save_price_range(self.public_profile_id, min_price, max_price, price_unit)
        if result['success']:            
            self.domain.update_price_range(min_price, max_price, price_unit)
            return {'success': True, 'message': '가격 범위가 성공적으로 저장되었습니다.'}
        
        print(f"가격 범위 업데이트 실패: result={result}")
        return {'success': False, 'message': '가격 범위 저장에 실패했습니다.'}

    # 계좌 정보 업데이트
    def update_account_info(self, bank_name, account_number, account_holder, account_type):
        hashed_account_number = EncryptionUtils.hash_password(account_number)
        
        result = self.repository.save_account_info(self.public_profile_id, bank_name, hashed_account_number, account_holder, account_type)
        if result['success']:            
            self.domain.update_account_info(bank_name, account_number, account_holder, account_type)
            return {'success': True, 'message': '계좌 정보가 성공적으로 저장되었습니다.'}
        
        print(f"계좌 정보 업데이트 실패: result={result}")
        return {'success': False, 'message': '계좌 정보 저장에 실패했습니다.'}
    
    def update_preferred_work_style(self, preferred_codes: Optional[list], deleted_preferred_codes: Optional[list]):
        # 선호 업무 스타일 추가 처리
        if preferred_codes:
            for code in preferred_codes:
                preferred_style = PreferredWorkStyleMapping(
                    public_profile_id=self.public_profile_id,
                    preferred_code=code
                )
                result = self.repository.save_preferred_work_style(preferred_style)
                if not result['success']:
                    print(f"선호 업무 스타일 추가 처리 실패: result={result}")
                    return {'success': False, 'message': f'{code} 선호 업무 스타일 저장에 실패했습니다.'}
                # 도메인 객체 업데이트
                self.domain.add_preferred_work_style(preferred_style)

        # 선호 업무 스타일 삭제 처리
        if deleted_preferred_codes:
            for code in deleted_preferred_codes:                
                preferred_style = PreferredWorkStyleMapping(
                    public_profile_id=self.public_profile_id,
                    preferred_code=code
                )
                result = self.repository.delete_preferred_work_style(preferred_style)
                if not result['success']:
                    print(f"선호 업무 스타일 삭제 처리 실패: result={result}")
                    return {'success': False, 'message': f'{code} 선호 업무 스타일 삭제에 실패했습니다.'}
                # 도메인 객체 업데이트
                self.domain.remove_preferred_work_style(preferred_style)

        return {'success': True, 'message': '선호 업무 스타일이 성공적으로 업데이트되었습니다.'}
    
    # 리뷰 등록
    def add_review(self, freelancer_user_id: str, review_title: str, review_text: str, rating: int, client_user_id: str):
        try:
            # freelancer_user_id를 통해 public_profile_id 가져오기
            result = self.repository.get_public_profile_id(freelancer_user_id)

            if not result['success']:
                return {'success': False, 'message': '사용자의 공개 프로필을 찾을 수 없습니다.'}

            public_profile_id = result['public_profile_id']
            
            # 새로운 리뷰 객체 생성
            review = Review(
                public_profile_id=public_profile_id,
                review_title=review_title,
                review_text=review_text,
                rating=rating,
                client_user_id=client_user_id
            )

            # 리뷰 저장 및 요약 업데이트 (레포지토리 계층에서 처리)
            save_result = self.repository.save_review(review)

            if save_result['success']:
                return {'success': True, 'message': '리뷰와 요약이 성공적으로 추가되었습니다.'}
            else:
                return {'success': False, 'message': '리뷰와 요약 추가에 실패했습니다.'}
        
        except Exception as e:
            return {'success': False, 'message': f'리뷰 추가 중 오류 발생: {str(e)}'}

    # 리뷰 삭제
    def delete_review(self, freelancer_user_id: str, review_title: str, review_text: str, rating: int, client_user_id: str):
        try:
            # freelancer_user_id를 통해 public_profile_id 가져오기
            result = self.repository.get_public_profile_id(freelancer_user_id)

            if not result['success']:
                return {'success': False, 'message': '사용자의 공개 프로필을 찾을 수 없습니다.'}

            public_profile_id = result['public_profile_id']

            # 리뷰 삭제 및 요약 업데이트 (레포지토리 계층에서 처리)
            delete_result = self.repository.delete_review(public_profile_id, client_user_id, review_title)

            if delete_result['success']:
                return {'success': True, 'message': '리뷰와 요약이 성공적으로 삭제되었습니다.'}
            else:
                return {'success': False, 'message': '리뷰와 요약 삭제에 실패했습니다.'}
        
        except Exception as e:
            return {'success': False, 'message': f'리뷰 삭제 중 오류 발생: {str(e)}'}
    
    # 매칭횟수 업데이트
    def update_match_count(self, freelancer_user_id: str, match_count: int):
        # freelancer_user_id를 통해 public_profile_id 가져오기
        result = self.repository.get_public_profile_id_by_user_id(freelancer_user_id)
        
        if not result['success']:
            return {'success': False, 'message': '사용자의 공개 프로필을 찾을 수 없습니다.'}

        public_profile_id = result['public_profile_id']

        # match_count 업데이트
        update_result = self.repository.save_match_count(public_profile_id, match_count)
        
        if update_result['success']:
            return {'success': True, 'message': '매치 카운트가 성공적으로 저장되었습니다.'}
        
        return {'success': False, 'message': '매치 카운트 저장에 실패했습니다.'}
    