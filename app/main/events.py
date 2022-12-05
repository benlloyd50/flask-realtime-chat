""" Events.py
    These are events that are called from javascript sockets and respond accordingly

    NOTE: The names `message`, `json`, `connect` and `disconnect` are reserved
"""
from flask import session
from flask_socketio import join_room, leave_room, emit
from .. import socketio
from .db import get_db
from html import escape
import time


@socketio.on("joined", namespace="/chat")
def joined(message: dict):
    room = session.get("room")
    username = session.get("username")

    join_server_and_load_chat(username, room)


@socketio.on("switched", namespace="/chat")
def switched(message: dict):
    username = session["username"]
    old_room = session["room"]

    new_room = message["server_id"]

    if new_room == old_room:
        return

    leave_room(old_room)
    emit("status", {"msg": " has left the server.", "name": username}, room=old_room)

    join_server_and_load_chat(username, new_room)
    session["room"] = new_room


@socketio.on("text", namespace="/chat")
def text(message: dict):
    room = session.get("room")
    username = session.get("username")
    user_id = session.get("user_id")

    ascii_msg = escape(message["msg"])

    emit("message", {"msg": ascii_msg, "name": username}, room=room)

    db = get_db()
    q = f"INSERT INTO chat VALUES('{ascii_msg}', '{user_id}', '{time.time()}', '{room}');"
    db.execute(q)
    db.commit()


@socketio.on("left", namespace="/chat")
def left(message: dict):
    room = session.get("room")
    username = session.get("username")
    leave_room(room)
    emit("status", {"msg": " has left the server.", "name": username}, room=room)


# Common Event Helper Functions
# Useful patterns that appear frequently are conviently a function, should not be called from outside this file


def join_server_and_load_chat(username, new_room):
    """Joins the `new_room` server and takes care of loading that room's chat"""
    db = get_db()
    query = f"""SELECT user.name as name, msg, time_sent
                FROM chat 
                    INNER JOIN user ON user.id = chat.user_id
                WHERE server_id = '{new_room}'
                ORDER BY time_sent ASC;"""
    db.row_factory = make_dicts
    chat_history = db.execute(query).fetchall()
    db.commit()

    # add self to new room
    join_room(new_room)
    for chat in chat_history:
        chat['time_sent'] = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(chat['time_sent']))
    emit("load_chat_history", chat_history)
    emit("status", {"msg": " has entered the server.", "name": username}, room=new_room)


def make_dicts(cursor, row):
    """Used as a row_factory function, use if dict is preferred over sqlite3.row"""
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
