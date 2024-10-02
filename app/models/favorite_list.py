from app import db

class FavoriteList(db.Model):
    __tablename__ = 'FAVORITE_LIST'
    
    favorite_list_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False)  
    author_id = db.Column(db.String(20), db.ForeignKey('USER_INFORMATION.user_id', ondelete='CASCADE'), nullable=False) 
    favorite_post_id = db.Column(db.String(50))
    category = db.Column(db.Enum('Project', 'Public Profile', 'Client'))
    
    user = db.relationship('UserInformation', foreign_keys=[user_id], backref=db.backref('favorite_lists', lazy=True, cascade="all, delete-orphan"))
    author = db.relationship('UserInformation', foreign_keys=[author_id], backref=db.backref('authored_favorites', lazy=True, cascade="all, delete-orphan"))
