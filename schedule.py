from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import hashlib

app = Flask(__name__)
app.config['DATABASE'] = 'userdata.db'

# Function to get the SQLite connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

# Function to close the SQLite connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('login.html')


# Define the login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    if user:
        #do hashing later
        stored_password_hash = user[2]
        input_password_hash = password

        if stored_password_hash == input_password_hash:
            # Authentication successful
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed
            return "Invalid username or password"
    else:
        # User not found
        return "Invalid username or password"

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
