from app import db

class PreferredKeywords(db.Model):
    __tablename__ = 'PREFERRED_KEYWORDS'
    
    preferred_code = db.Column(db.String(20), primary_key=True)
    preferred_type = db.Column(db.String(50), nullable=False)
    preferred_name = db.Column(db.String(100), nullable=False)
