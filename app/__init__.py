""" This code was taken from https://github.com/miguelgrinberg/Flask-SocketIO-Chat
    and modified for educational use
"""
from flask import Flask, render_template
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=True):
    app = Flask(__name__)
    app.debug = debug
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    # Session(app)
    # from . import db
    # db.init_app(app)
    socketio.init_app(app)
    return app