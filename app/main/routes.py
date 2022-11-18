from flask import redirect, render_template, request, session, url_for

from . import main
from .forms import LoginForm, RegisterForm

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['password'] = form.password.data
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
        session['username'] = form.name.data
        session['password'] = form.password.data
        session['room'] = 'default'
        return redirect(url_for('.chat'))
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
