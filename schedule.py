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
    return render_template('index.html')  
    
#after a button is pressed, redirect to that html page
@app.route('/redirect/<destination>')
def redirect_page(destination):
    if destination == 'signup':
        return redirect(url_for('signup_page'))
    elif destination == 'login':
        return redirect(url_for('login_page'))

#html pages for login and signup pages
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

#functions for when you post the form
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['password2']
    
    if password == confirm_password:
        db = get_db()
        cur = db.cursor()

        cur.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))
        db.commit()
        return redirect(url_for('dashboard'))
    
    else:
        return "Passwords do not match"

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
