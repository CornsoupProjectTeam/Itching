from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ClientPostReferenceImageMapping(db.Model):
    __tablename__ = 'CLIENT_POST_REFERENCE_IMAGE_MAPPING'
    
    client_post_id = db.Column(db.String(50), db.ForeignKey('CLIENT_POST.client_post_id'), primary_key=True)
    reference_image_path = db.Column(db.String(255))
    
    client_post = db.relationship('ClientPost', backref=db.backref('reference_images', uselist=False))
