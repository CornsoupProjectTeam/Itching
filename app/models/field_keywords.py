from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FieldKeywords(db.Model):
    __tablename__ = 'FIELD_KEYWORDS'
    
    field_code = db.Column(db.String(20), primary_key=True)
    field_type = db.Column(db.String(50), nullable=False)
    field_name = db.Column(db.String(100), unique=True, nullable=False)
