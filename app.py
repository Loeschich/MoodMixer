from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'  # Für Session-Management

USERS_FILE = 'users.json'

# Stelle sicher, dass die Datei existiert
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)


def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_users()
        if email in users:
            flash('Email ist bereits registriert.')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        users[email] = {'password': hashed_pw}
        save_users(users)
        flash('Registrierung erfolgreich! Bitte einloggen.')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    users = load_users()
    if email in users and check_password_hash(users[email]['password'], password):
        session['user'] = email
        return redirect(url_for('home'))
    else:
        flash('Ungültige Login-Daten.')
        return redirect(url_for('index'))


@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', email=session['user'])
    else:
        flash('Bitte erst einloggen.')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
