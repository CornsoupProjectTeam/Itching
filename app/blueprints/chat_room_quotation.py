#견적서 : Chat_room_quotation 

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.Config')

    # Initialize MongoDB
    mongo.init_app(app)

    # Register Blueprints
    from app.routes.chat_routes import chat_bp
    app.register_blueprint(chat_bp)

    return app
