import sqlite3
from flask import redirect, render_template, request, session, url_for
from .db import get_db
import hashlib
import uuid

from . import main
from .auth import login_required
from .forms import LoginForm, RegisterForm


@main.route("/", methods=["GET", "POST"])
def landing_page():
    return render_template("landingpage.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = str(uuid.uuid4())
        username: str = form.name.data
        plaintext_pass: str = form.password.data
        hashed_password = hashlib.md5(plaintext_pass.encode()).hexdigest()

        db = get_db()
        sql_query = (
            f"INSERT INTO user VALUES('{user_id}','{username}', '{hashed_password}');"
        )
        try:
            db.execute(sql_query)
            db.commit()
        except sqlite3.IntegrityError as er:
            error = "Error: username already exist!"
            return render_template("index.html", form=form, error=error)

        session["username"] = form.name.data
        session["user_id"] = user_id
        session["password"] = form.password.data
        session["room"] = "Default"
        return redirect(url_for(".chat"))
    elif request.method == "GET":
        form.name.data = session.get("name", "")

    return render_template("index.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    """Login form to enter a room."""

    form = LoginForm()
    error = ""
    if form.validate_on_submit():
        password_plaintext = form.password.data
        username = form.name.data
        hashed_password = hashlib.md5(password_plaintext.encode()).hexdigest()

        db = get_db()
        query = f"SELECT * FROM user WHERE password = '{hashed_password}' AND name = '{username}';"
        user = db.execute(query).fetchone()
        db.commit()

        if user is None:
            error = "Username or password did not match."
        else:
            session.clear()  # start with a new session
            session["username"] = form.name.data
            session["password"] = form.password.data
            session["user_id"] = user["id"]
            session["room"] = "Default"
            return redirect(url_for(".chat"))

    elif request.method == "GET":
        form.name.data = session.get(
            "username", ""
        )  # attempt to fill with last entered name

    return render_template("index.html", form=form, error=error)


@main.route("/chat")
@login_required
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    db = get_db()

    name = session.get("username", "")
    room = session.get("room", "SESSION_UNASSIGNED_ROOM")

    # if no name or room is set, return them to the login
    if name == "" or room == "":
        return redirect(url_for(".login"))

    sql_query = "SELECT name FROM server;"
    servers = db.execute(sql_query).fetchall()
    db.commit()

    # print(f"Servers: {servers}")

    server_list = list()
    for serv in servers:
        server_list.append(serv[0])

    # print(f"Server list: {server_list}")

    return render_template("chat.html", name=name, room=room, servers=server_list)
