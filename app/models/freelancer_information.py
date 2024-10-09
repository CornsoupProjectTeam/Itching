from app import db
from datetime import datetime

class PublicProfile(db.Model):
    __tablename__ = 'PUBLIC_PROFILE'
    
    public_profile_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    profile_image_path = db.Column(db.String(255))
    freelancer_intro_one_liner = db.Column(db.String(100))
    freelancer_intro = db.Column(db.Text)
    project_duration = db.Column(db.Integer)
    freelancer_badge = db.Column(db.Enum('Gold', 'Silver', 'Bronze'), default='Bronze')
    match_count = db.Column(db.Integer, default=0)
    sns_link = db.Column(db.String(255))
    average_response_time = db.Column(db.Integer)
    freelancer_registration_date = db.Column(db.DateTime)
    public_profile_registration_st = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_information = db.relationship('UserInformation', backref=db.backref('public_profiles', lazy=True, cascade="all, delete-orphan"))

class PublicProfileList(db.Model):
    __tablename__ = 'PUBLIC_PROFILE_LIST'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    profile_image_path = db.Column(db.String(255))
    freelancer_badge = db.Column(db.Enum('Gold', 'Silver', 'Bronze'))
    match_count = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Integer)
    freelancer_registration_date = db.Column(db.DateTime)
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    public_profile_registration_st = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('public_profile_lists', uselist=False, cascade="all, delete-orphan"))

class FreelancerExpertiseFieldMapping(db.Model):
    __tablename__ = 'FREELANCER_EXPERTISE_FIELD_MAPPING'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    field_code = db.Column(db.String(20), db.ForeignKey('FIELD_KEYWORDS.field_code', ondelete='CASCADE'), primary_key=True)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('expertise_fields', lazy=True, cascade="all, delete-orphan"))
    field_keywords = db.relationship('FieldKeywords', backref=db.backref('freelancer_expertise_mappings', lazy=True, cascade="all, delete-orphan"))

class FreelancerSkillMapping(db.Model):
    __tablename__ = 'FREELANCER_SKILL_MAPPING'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    skill_code = db.Column(db.String(20), db.ForeignKey('SKILL_KEYWORDS.skill_code', ondelete='CASCADE'), primary_key=True)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('skills', lazy=True, cascade="all, delete-orphan"))
    skill_keywords = db.relationship('SkillKeywords', backref=db.backref('freelancer_skills_mappings', lazy=True, cascade="all, delete-orphan"))

class FreelancerEducationMapping(db.Model):
    __tablename__ = 'FREELANCER_EDUCATION_MAPPING' 
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('educations', lazy=True, cascade="all, delete-orphan"))

class FreelancerCareerMapping(db.Model):
    __tablename__ = 'FREELANCER_CAREER_MAPPING'
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('careers', lazy=True, cascade="all, delete-orphan"))

class FreelancerPortfolioMapping(db.Model):
    __tablename__ = 'FREELANCER_PORTFOLIO_MAPPING'  
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False)  
    image_path = db.Column(db.String(255), nullable=True) 
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('portfolios', cascade="all, delete-orphan", lazy=True))

class FreelancerServiceOptions(db.Model):
    __tablename__ = 'FREELANCER_SERVICE_OPTIONS'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    weekend_consultation = db.Column(db.Boolean, default=False)
    weekend_work = db.Column(db.Boolean, default=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('service_options', uselist=False, cascade="all, delete-orphan"))

class FreelancerPriceRange(db.Model):
    __tablename__ = 'FREELANCER_PRICE_RANGE'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    min_price = db.Column(db.Numeric(10, 2), nullable=False)
    max_price = db.Column(db.Numeric(10, 2), nullable=False)
    price_unit = db.Column(db.Enum('KRW', 'USD'), default='KRW')
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('price_range', uselist=False, cascade="all, delete-orphan"))

class PreferredWorkStyleMapping(db.Model):
    __tablename__ = 'PREFERRED_WORK_STYLE_MAPPING'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    preferred_code = db.Column(db.String(20), db.ForeignKey('PREFERRED_KEYWORDS.preferred_code', ondelete='CASCADE'), primary_key=True)

    public_profile = db.relationship('PublicProfile', backref=db.backref('preferred_work_styles', lazy=True, cascade="all, delete-orphan"))
    preferred_keyword = db.relationship('PreferredKeywords', backref=db.backref('preferred_work_style_mappings', lazy=True, cascade="all, delete-orphan"))

class FreelancerAccountInfo(db.Model):
    __tablename__ = 'FREELANCER_ACCOUNT_INFO'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    bank_name = db.Column(db.String(50), nullable=False)
    account_number = db.Column(db.String(255), nullable=False)
    account_holder = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.Enum('Personal', 'Corporation'), nullable=False)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('account_info', uselist=False, cascade="all, delete-orphan"))

class Review(db.Model):
    __tablename__ = 'REVIEW'
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), nullable=False)
    client_user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)
    review_title = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('reviews', lazy=True, cascade="all, delete-orphan"))
    client_user = db.relationship('UserInformation', backref=db.backref('client_reviews', lazy=True, cascade="all, delete-orphan"))

class ReviewSummary(db.Model):
    __tablename__ = 'REVIEW_SUMMARY'
    
    public_profile_id = db.Column(db.String(50), db.ForeignKey('PUBLIC_PROFILE.public_profile_id', ondelete='CASCADE'), primary_key=True)
    total_reviews = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    
    public_profile = db.relationship('PublicProfile', backref=db.backref('review_summary', uselist=False, cascade="all, delete-orphan"))
