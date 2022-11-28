""" This code was taken from https://github.com/miguelgrinberg/Flask-SocketIO-Chat
    and modified for educational use
"""
from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
import os

socketio = SocketIO()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SESSION_TYPE='filesystem',
        DATABASE=os.path.join(app.instance_path, 'vox.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        # presumably this should only be an issue if the folder was made
        pass

    # Creates server-side session information
    Session(app)
    
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .main import db
    db.init_app(app)

    socketio.init_app(app, manage_session=False)
    return app