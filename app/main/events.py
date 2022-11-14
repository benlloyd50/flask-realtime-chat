from flask import session
from flask_socketio import join_room, leave_room, emit
from .. import socketio 


@socketio.on('joined', namespace="/chat")
def joined(message):
    room = session.get("room")
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + " : " + message['msg']}, room=room)

@socketio.on('left', namespace="/chat")
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    emit("status", {'msg': username + " has left the server."}, room=room)