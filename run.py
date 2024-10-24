# import os
# import eventlet
# eventlet.monkey_patch()  # 반드시 가장 첫 줄에 위치해야 합니다.

# from app import app, socketio  # 이미 초기화된 app과 socketio를 가져옴

# if __name__ == "__main__":
#     # Flask-SocketIO 서버 실행
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)

# run.py
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO

# app = Flask(__name__)
app = Flask(__name__, template_folder='app/templates')
socketio = SocketIO(app, cors_allowed_origins="*")

# 기본 경로('/') 처리
@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
