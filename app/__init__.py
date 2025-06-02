import sqlite3
import json
from flask import Flask, g, current_app
import click

# Function to get a database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

# Function to close the database connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# CLI command to initialize the user table
@click.command('init-db')
def init_db_command():
    db = sqlite3.connect(current_app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )"""
    )
    db.commit()
    db.close()
    click.echo('Initialized the database.')

# Register init-db command and teardown function in app context
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

from .ollama_client import build_prompt, call_ollama
from .auth import auth_bp
from .routes import main_bp


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.Config')

    # Initialize the database (CLI init-db command)
    init_app(app)

    # Load questions from JSON file
    with open(app.config['QUESTIONS_JSON'], 'r', encoding='utf-8') as f:
        app.questions = json.load(f)

    # Register blueprints for authentication and main routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    return app