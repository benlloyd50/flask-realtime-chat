from flask import Blueprint

main = Blueprint('main', __name__)

from . import events, routes 

# def create_app():
#     from . import db
#     db.init_app(app)
    
#     return app