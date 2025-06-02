import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect(current_app.config['DATABASE'])
        cursor = db.cursor()
        error = None
        # Validate form inputs
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            cursor.execute('SELECT id FROM user WHERE username = ?', (username,))
            if cursor.fetchone() is not None:
                error = f'User {username} is already registered.'
        # If no validation errors, create new user
        if error is None:
            hashed = generate_password_hash(password)
            cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, hashed))
            db.commit()
            db.close()
            return redirect(url_for('auth.login'))
        flash(error)
        db.close()
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect(current_app.config['DATABASE'])
        cursor = db.cursor()
        error = None
        cursor.execute('SELECT id, password FROM user WHERE username = ?', (username,))
        user = cursor.fetchone()
        # Check if user exists and password matches
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[1], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            db.close()
            return redirect(url_for('main.question', qid=0))
        flash(error)
        db.close()
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))