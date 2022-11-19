""" This code was taken from https://github.com/miguelgrinberg/Flask-SocketIO-Chat
    and modified for educational use
"""
from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SESSION_TYPE='filesystem'
    )
    # Creates server-side session information
    Session(app)
    
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    socketio.init_app(app, manage_session=False)
    return app