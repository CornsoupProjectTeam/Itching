from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProjectImageMapping(db.Model):
    __tablename__ = 'PROJECT_IMAGE_MAPPING'
    
    project_id = db.Column(db.String(50), db.ForeignKey('PROJECT_INFO.project_id', ondelete='CASCADE'), primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    
    project = db.relationship('ProjectInfo', backref=db.backref('images', cascade="all, delete-orphan", lazy=True))

