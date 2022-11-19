from flask import redirect, render_template, request, session, url_for
import sqlite3
import hashlib
import uuid
import os

from . import main
from .forms import LoginForm, RegisterForm

curr_dir = os.path.dirname(os.path.abspath(__file__))
db_connection = sqlite3.connect(curr_dir + "\database.db", check_same_thread=False)
cursor = db_connection.cursor()

@main.route('/register', methods=['GET', 'POST'])
def register():
    user_id = str(uuid.uuid4())
    form = RegisterForm()
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['password'] = form.password.data
        hashed_password = hashlib.md5(session['password'].encode()).hexdigest()
        sql_query = "INSERT INTO user VALUES('{id}','{un}', '{pw}');".format(id = user_id, un = session['username'], pw = hashed_password)
        cursor.execute(sql_query)
        db_connection.commit()
        # cursor.close()
        session['room'] = 'default'
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.password.data = session.get('password', '')
    return render_template('index.html', form=form)
    # TODO - check and store in database
   

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        hashed_password = hashlib.md5(form.password.data.encode()).hexdigest()
        sql_query = "SELECT * FROM user WHERE u_password = '{hP}' AND username = '{un}';".format(hP = hashed_password, un = form.name.data)
        result = cursor.execute(sql_query)
        result = result.fetchall()
        db_connection.commit()
        # cursor.close()
        if result:
            session['username'] = form.name.data
            session['password'] = form.password.data
            session['room'] = 'default'
            return redirect(url_for('.chat'))
        else:
            error = "Error: Username or password do not match!"
            return render_template('index.html', form=form, error=error)
        
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.password.data = session.get('password', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('username', '')
    room = session.get('room', 'SESSION_UNASSIGNED_ROOM')
    # print(f"In chat we got room {room}")

    # if no name or room is set, return them to the login
    if name == '' or room == '':
        return redirect(url_for('.login'))

    # TODO get user's server from db, this is what the response from the db should sorta look like
    servers = ['Default', 'Testing', 'CSC 354']


    return render_template('chat.html', name=name, room=room, servers=servers)

# cursor.close()