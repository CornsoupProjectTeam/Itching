from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PretestCondition(db.Model):
    __tablename__ = 'PRETEST_CONDITION'
    
    version_code = db.Column(db.String(20), primary_key=True)
    sequence = db.Column(db.Integer, primary_key=True)
    requirement = db.Column(db.Text)
