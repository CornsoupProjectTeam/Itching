from app import db

class ProjectImageMapping(db.Model):
    __tablename__ = 'PROJECT_IMAGE_MAPPING'
    
    sequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('PROJECT_INFO.project_id', ondelete='CASCADE'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    
    project = db.relationship('ProjectInfo', backref=db.backref('images', cascade="all, delete-orphan", lazy=True))
