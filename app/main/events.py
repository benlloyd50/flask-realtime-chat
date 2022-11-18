""" Events.py
    These are events that are called from javascript sockets and respond accordingly

    NOTE: The names `message`, `json`, `connect` and `disconnect` are reserved
"""
from flask import session
from flask_socketio import join_room, leave_room, emit
from .. import socketio 


@socketio.on('joined', namespace="/chat")
def joined(message: dict):
    room = session.get("room")
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)

@socketio.on('switched', namespace="/chat")
def switched(message: dict):
    username = session['username']
    old_room = session['room']

    leave_room(old_room)
    emit("status", {'msg': f"{username} has left the server."}, room=old_room)

    # add self to new room
    new_room = message['server_id']
    print(f"Session room was updated to {new_room}")
    session['room'] = new_room
    join_room(new_room)
    emit('status', {'msg': f'{username} has entered the room.'}, room=new_room)

@socketio.on('text', namespace='/chat')
def text(message: dict):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + " : " + message['msg']}, room=room)

@socketio.on('left', namespace="/chat")
def left(message: dict):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    emit("status", {'msg': username + " has left the server."}, room=room)