from app.models.freelancer_information import *
from sqlalchemy.exc import SQLAlchemyError

class FreelancerInformationRepository:

    # user_id로 public_profile 존재 여부를 확인하는 메서드
    def get_public_profile_id(self, user_id):
        try:
            public_profile = PublicProfile.query.filter_by(user_id=user_id).first()
            
            # 프로필이 존재하면 success와 함께 public_profile_id 반환, 없으면 False 반환
            if public_profile:
                return {'success': True, 'public_profile_id': public_profile.public_profile_id}
            else:
                return {'success': False, 'message': '공개 프로필이 없습니다.'}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    def get_public_profile_for_freelancer_information(self, public_profile_id):
        try:
            # public_profile을 가져옴
            public_profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            
            if not public_profile:
                return {'success': False, 'message': '공개 프로필을 찾을 수 없습니다.'}

            # 각 맵핑 테이블에서 public_profile_id를 기준으로 데이터 가져옴
            
            service_options = FreelancerServiceOptions.query.filter_by(public_profile_id=public_profile_id).first()

            price_range = FreelancerPriceRange.query.filter_by(public_profile_id=public_profile_id).first()
            
            preferred_work_style = PreferredWorkStyleMapping.query.filter_by(public_profile_id=public_profile_id).all()
            
            account_info = FreelancerAccountInfo.query.filter_by(public_profile_id=public_profile_id).first()
            
            review = Review.query.filter_by(public_profile_id=public_profile_id).all()
            
            review_summary = ReviewSummary.query.filter_by(public_profile_id=public_profile_id).first()

            # 데이터를 딕셔너리 형태로 반환
            return {
                'success': True,
                'profile': public_profile,
                'service_options': service_options,
                'price_range': price_range,
                'preferred_work_style': preferred_work_style,
                'account_info': account_info,
                'review': review,
                'review_summary': review_summary
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    # PublicProfileList 가져오기
    def get_public_profile_list(self, public_profile_id: str):
        try:
                profile_list = PublicProfileList.query.filter_by(public_profile_id=public_profile_id).first()
                if profile_list:
                    return {"success": True, "profile_list": profile_list}
                return {"success": False, "message": "프로필 리스트를 찾을 수 없습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"프로필 리스트 조회 중 오류 발생: {str(e)}"}

    # 프로젝트 기간 저장
    def save_project_duration(self, public_profile_id, project_duration):
        try:            
            profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if profile:                
                profile.project_duration = project_duration
                db.session.commit()
                return {"success": True, "message": "프로젝트 기간이 성공적으로 저장되었습니다."}
            return {"success": False, "message": "프로필을 찾을 수 없습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"프로젝트 기간 저장에 실패했습니다: {str(e)}"}

    # 공개 프로필 등록 상태 저장
    def save_public_profile_registration_st(self, public_profile_id, registration_status):
        try:           
            profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if profile:            
                profile.public_profile_registration_st = registration_status
                db.session.commit()
                return {"success": True, "message": "등록 상태가 성공적으로 저장되었습니다."}
            return {"success": False, "message": "프로필을 찾을 수 없습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"등록 상태 저장에 실패했습니다: {str(e)}"}

    # 프리랜서 소개 한 줄 저장
    def save_freelancer_intro_one_liner(self, public_profile_id, intro_one_liner):
        try:
            profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if profile:
                # 프리랜서 소개 업데이트
                profile.freelancer_intro_one_liner = intro_one_liner
                db.session.commit()
                return {"success": True, "message": "프리랜서 소개가 성공적으로 저장되었습니다."}
            return {"success": False, "message": "프로필을 찾을 수 없습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"프리랜서 소개 저장에 실패했습니다: {str(e)}"}
    
    # 서비스 옵션 저장
    def save_serviceoptions(self, public_profile_id, weekend_consultation, weekend_work):
        try:
            profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if not profile:
                return {"success": False, "message": "공개 프로필을 찾을 수 없습니다."}

            # 서비스 옵션이 없을 경우 생성
            if not profile.service_options:  # 수정된 부분
                service_options = FreelancerServiceOptions(
                    public_profile_id=public_profile_id,
                    weekend_consultation=weekend_consultation,
                    weekend_work=weekend_work
                )
                db.session.add(service_options)
            else:
                # 서비스 옵션이 존재하면 업데이트
                profile.service_options.weekend_consultation = weekend_consultation
                profile.service_options.weekend_work = weekend_work
            
            db.session.commit()
            return {"success": True, "message": "서비스 옵션이 성공적으로 저장되었습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"서비스 옵션 저장에 실패했습니다: {str(e)}"}

    # 가격 범위 저장
    def save_price_range(self, public_profile_id, min_price, max_price, price_unit):
        try:
            profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if not profile:
                return {"success": False, "message": "공개 프로필을 찾을 수 없습니다."}

            # 가격 범위가 없을 경우 생성
            if not profile.price_range:
                profile.price_range = FreelancerPriceRange(
                    public_profile_id=public_profile_id,
                    min_price=min_price,
                    max_price=max_price,
                    price_unit=price_unit
                )
                db.session.add(profile.price_range)
            else:
                # 가격 범위가 존재하면 업데이트
                profile.price_range.min_price = min_price
                profile.price_range.max_price = max_price
                profile.price_range.price_unit = price_unit
            
            db.session.commit()
            return {"success": True, "message": "가격 범위가 성공적으로 저장되었습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"가격 범위 저장에 실패했습니다: {str(e)}"}

    # 계좌 정보 저장
    def save_account_info(self, public_profile_id, bank_name, account_number, account_holder, account_type):
        try:
            profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if not profile:
                return {"success": False, "message": "공개 프로필을 찾을 수 없습니다."}

            # 계좌 정보가 없을 경우 생성
            if not profile.account_info:
                profile.account_info = FreelancerAccountInfo(
                    public_profile_id=public_profile_id,
                    bank_name=bank_name,
                    account_number=account_number,
                    account_holder=account_holder,
                    account_type=account_type
                )
                db.session.add(profile.account_info)
            else:
                # 계좌 정보가 존재하면 업데이트
                profile.account_info.bank_name = bank_name
                profile.account_info.account_number = account_number
                profile.account_info.account_holder = account_holder
                profile.account_info.account_type = account_type
            
            db.session.commit()
            return {"success": True, "message": "계정 정보가 성공적으로 저장되었습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"계정 정보 저장에 실패했습니다: {str(e)}"}
    
    # 선호 업무 스타일 저장
    def save_preferred_work_style(self, preferred_style):
        try:
            db.session.add(preferred_style)
            db.session.commit()
            return {"success": True, "message": "선호 업무 스타일이 성공적으로 저장되었습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"선호 업무 스타일 저장에 실패했습니다: {str(e)}"}
        
    # 선호 업무 스타일 삭제
    def delete_preferred_work_style(self, preferred_style):
        try:
            # 데이터베이스에서 삭제할 선호 업무 스타일 검색
            existing_style = PreferredWorkStyleMapping.query.filter_by(
                public_profile_id=preferred_style.public_profile_id,
                preferred_code=preferred_style.preferred_code
            ).first()
            
            if existing_style:
                db.session.delete(existing_style)
                db.session.commit()
                return {"success": True, "message": "선호 업무 스타일이 성공적으로 삭제되었습니다."}
            return {"success": False, "message": "삭제할 선호 업무 스타일을 찾을 수 없습니다."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"선호 업무 스타일 삭제에 실패했습니다: {str(e)}"}
        
    def save_match_count(self, public_profile_id: str, match_count: int):
        try:
            # PublicProfile 검색
            profile = PublicProfile.query.filter_by(public_profile_id=public_profile_id).first()
            if profile:
                # PublicProfile의 match_count 업데이트
                profile.match_count = match_count

                # PublicProfileList의 match_count 업데이트
                public_profile_list = PublicProfileList.query.filter_by(public_profile_id=public_profile_id).first()
                if public_profile_list:
                    public_profile_list.match_count = match_count

                # 세션 커밋
                db.session.commit()
                return {"success": True, "message": "매치 카운트가 성공적으로 저장되었습니다."}
            
            return {"success": False, "message": "공개 프로필을 찾을 수 없습니다."}
        
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"매치 카운트 저장에 실패했습니다: {str(e)}"}
    
    def save_review(self, review: Review):
        try:
            # 리뷰 저장
            db.session.add(review)

            # 리뷰 요약 업데이트
            reviews = Review.query.filter_by(public_profile_id=review.public_profile_id).all()
            total_reviews = len(reviews)
            average_rating = round(sum(r.rating for r in reviews) / total_reviews, 2) if total_reviews > 0 else 0.00

            # ReviewSummary 업데이트 또는 생성
            review_summary = ReviewSummary.query.filter_by(public_profile_id=review.public_profile_id).first()
            if review_summary:
                review_summary.total_reviews = total_reviews
                review_summary.average_rating = average_rating
            else:
                review_summary = ReviewSummary(
                    public_profile_id=review.public_profile_id,
                    total_reviews=total_reviews,
                    average_rating=average_rating
                )
                db.session.add(review_summary)

            # PublicProfileList의 average_rating 업데이트
            public_profile_list = PublicProfileList.query.filter_by(public_profile_id=review.public_profile_id).first()
            if public_profile_list:
                public_profile_list.average_rating = average_rating
            else:
                public_profile_list = PublicProfileList(
                    public_profile_id=review.public_profile_id,
                    average_rating=average_rating
                )
                db.session.add(public_profile_list)

            # 모든 변경 사항을 한 번에 커밋
            db.session.commit()
            return {"success": True, "message": "리뷰와 요약이 성공적으로 저장되었습니다."}
        
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"리뷰 저장에 실패했습니다: {str(e)}"}

    def delete_review(self, public_profile_id: str, client_user_id: str, review_title: str):
        try:
            # 해당 리뷰 검색 및 삭제
            review = Review.query.filter_by(
                public_profile_id=public_profile_id,
                client_user_id=client_user_id,
                review_title=review_title
            ).first()

            if review:
                db.session.delete(review)

                # 리뷰 요약 업데이트
                reviews = Review.query.filter_by(public_profile_id=public_profile_id).all()
                total_reviews = len(reviews)
                average_rating = round(sum(r.rating for r in reviews) / total_reviews, 2) if total_reviews > 0 else 0.00

                # ReviewSummary 업데이트 또는 생성
                review_summary = ReviewSummary.query.filter_by(public_profile_id=public_profile_id).first()
                if review_summary:
                    review_summary.total_reviews = total_reviews
                    review_summary.average_rating = average_rating
                else:
                    review_summary = ReviewSummary(
                        public_profile_id=public_profile_id,
                        total_reviews=total_reviews,
                        average_rating=average_rating
                    )
                    db.session.add(review_summary)

                # PublicProfileList의 average_rating 업데이트
                public_profile_list = PublicProfileList.query.filter_by(public_profile_id=public_profile_id).first()
                if public_profile_list:
                    public_profile_list.average_rating = average_rating
                else:
                    public_profile_list = PublicProfileList(
                        public_profile_id=public_profile_id,
                        average_rating=average_rating
                    )
                    db.session.add(public_profile_list)

                # 모든 변경 사항을 한 번에 커밋
                db.session.commit()
                return {"success": True, "deleted_review": review, "message": "리뷰와 요약이 성공적으로 삭제되었습니다."}
            
            return {"success": False, "message": "삭제할 리뷰를 찾을 수 없습니다."}
        
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"리뷰 삭제에 실패했습니다: {str(e)}"}
