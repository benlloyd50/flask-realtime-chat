""" Database declarations and useful functions
    Global variable holds the current active database of an instance and performs operations on it

    Query Examples
    
    Insert (*if unique values are involved a try except block is necessary)
        db = get_db()
        q = GENERIC SQL INSERT QUERY
        db.execute(q)
        db.commit()

    Select
        db = get_db()
        sql_query = GENERIC SQL SELECT QUERY
        user = db.execute(sql_query).fetchone() # or fetchall() for a list
        db.commit()
"""
import sqlite3

import click
from flask import current_app, g


def get_db():
    """Retrieve the global database object, connects to a database if none connected"""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Remove the database object active on global and close the connection"""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Creates a new database file on the system"""
    # TODO the webserver will need a way to initialize the database since this does not run automatically
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Console command Usage: flask init-db"""
    init_db()
    click.echo("Initialized the database")


def init_app(app):
    """App will automatically close the database when used after it returns the response"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
