from app import app, socketio

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, ssl_context='adhoc'