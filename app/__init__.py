from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend/build")
app.config.from_object('app.config')

# db = SQLAlchemy(app)
# mongo = PyMongo(app)
CORS(app)

from app import routes  # API 라우트 불러오기
