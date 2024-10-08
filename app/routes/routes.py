from flask import Blueprint
from app.routes.test_api import test_api_bp
from app.routes.react import react_bp
from app.routes.test_db import test_db_bp
from app.routes.user_information_route import user_information_bp
from app.routes.login_route import login_bp
from app.routes.payment_authentication_route import payment_authentication_bp
from app.routes.identitiy_verification_route import identity_verification_bp
from app.routes.freelancer_list_routes import freelancer_bp
from app.routes.client_post_routes import client_post_bp
from app.routes.chat_room_quotation_routes import quotation_bp
from app.routes.project_list_routes import project_list_bp
from app.routes.chat_room_routes import chat_room_bp 

def init_routes(app):
    app.register_blueprint(test_api_bp)
    app.register_blueprint(react_bp)
    app.register_blueprint(test_db_bp)
    app.register_blueprint(user_information_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(payment_authentication_bp)
    app.register_blueprint(identity_verification_bp)
    app.register_blueprint(freelancer_bp)
    app.register_blueprint(client_post_bp)
    app.register_blueprint(quotation_bp)
    app.register_blueprint(project_list_bp)
    app.register_blueprint(chat_room_bp)



