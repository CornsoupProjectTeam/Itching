from flask import Blueprint
from app.routes.test_api import test_api_bp
from app.routes.react import react_bp
from app.routes.test_db import test_db_bp

def init_routes(app):
    app.register_blueprint(test_api_bp)
    app.register_blueprint(react_bp)
    app.register_blueprint(test_db_bp)
