from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 모델 수동 Import
from app.models.login import Login
from app.models.email_notification import EmailNotification
from app.models.field_keywords import FieldKeywords
from app.models.preferred_keywords import PreferredKeywords
from app.models.skill_keywords import SkillKeywords
from app.models.user_information import UserInformation, ClientPreferredFieldMapping, PreferredFreelancerMapping
from app.models.user_consent import UserConsent
from app.models.freelancer_information import (
    PublicProfile,
    PublicProfileList,
    FreelancerExpertiseFieldMapping,
    FreelancerSkillMapping,
    FreelancerEducationMapping,
    FreelancerCareerMapping,
    FreelancerPortfolioMapping,
    FreelancerServiceOptions,
    FreelancerPriceRange,
    PreferredWorkStyleMapping,
    FreelancerAccountInfo
)
from app.models.chat_room_master import ChatRoomMaster
from app.models.chat_room_quotation import ChatRoomQuotation
from app.models.payment import Payment
from app.models.pretest_scanner import PretestScanner
from app.models.chat_room_scanner import ChatRoomScanner
from app.models.pretest_condition import PretestCondition
from app.models.pretest_scanner_requirement import PretestScannerRequirement
from app.models.chat_room_scanner_requirement import ChatRoomScannerRequirement
from app.models.project_info import ProjectInfo
from app.models.project_list import ProjectList

from app.models.client_explore import ClientPost, ClientPostList, ClientPostReferenceImageMapping


