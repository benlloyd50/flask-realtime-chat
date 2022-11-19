from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app)
    
    
# def create_app():
#     from .app import db
#     db.init_app(app)
    
#     return app