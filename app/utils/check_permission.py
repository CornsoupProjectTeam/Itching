from flask import session, abort

def check_permission(user_id):
    #세션에 저장된 user_id와 URI에 포함된 user_id가 동일한지 체크
    if 'user_id' not in session:
        abort(401, description="Unauthorized: User is not logged in.")
    if session['user_id'] != user_id:
        abort(403, description="Forbidden: You do not have access to this resource.")
