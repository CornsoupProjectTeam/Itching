# mysql_project_list.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProjectList(db.Model):
    __tablename__ = 'project_list'

    project_id = db.Column(db.String(50), primary_key=True)
    public_profile_id = db.Column(db.String(30), db.ForeignKey('public_profile.public_profile_id'), nullable=False)
    freelancer_user_id = db.Column(db.String(20), db.ForeignKey('login.user_id'), nullable=False)
    project_title = db.Column(db.String(200), nullable=False)
    field = db.Column(db.String(100), nullable=True)
    project_payment_amount = db.Column(db.Integer, nullable=False)
    main_image_path = db.Column(db.String(255), nullable=True)
    service_options = db.Column(db.Text, nullable=True)
    avg_response_time = db.Column(db.Integer, nullable=True)
    freelancer_badge = db.Column(db.String(10), nullable=True)
    avg_rating = db.Column(db.Numeric(3, 1), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    public_profile = db.relationship('PublicProfile', backref='projects')
    freelancer = db.relationship('Login', backref='projects')

    def __repr__(self):
        return self.project_id
