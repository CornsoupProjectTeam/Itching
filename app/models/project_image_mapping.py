from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProjectImageMapping(db.Model):
    __tablename__ = 'PROJECT_IMAGE_MAPPING'
    
    project_id = db.Column(db.String(50), db.ForeignKey('PROJECT_INFO.project_id'), primary_key=True)
    image_path = db.Column(db.String(255))
    
    project_info = db.relationship('ProjectInfo', backref=db.backref('image_mapping', uselist=False))
