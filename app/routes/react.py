from flask import Blueprint, send_from_directory, current_app

react_bp = Blueprint('react', __name__)

@react_bp.route('/', defaults={'path': ''})
@react_bp.route('/<path:path>')
def serve_react_app(path):
    if path != "" and path.startswith("static"):
        return send_from_directory(current_app.static_folder, path)
    elif path.endswith(".js") or path.endswith(".css") or path.endswith(".ico"):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, 'index.html')
