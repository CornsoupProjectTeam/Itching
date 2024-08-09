from flask import Flask, jsonify, send_from_directory
from app import app

# API 엔드포인트 예시
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello from Flask!",
        "status": "success"
    }
    return jsonify(data)

# React 정적 파일 제공 (index.html 등)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and path.startswith("static"):
        return send_from_directory(app.static_folder, path)
    elif path.endswith(".js") or path.endswith(".css") or path.endswith(".ico"):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
