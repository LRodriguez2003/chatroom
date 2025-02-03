from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# In-memory user data (for demonstration purposes)
users_db = {}

# Route to display the login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route to handle the login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the username exists and the password matches
    user = users_db.get(username)
    if user and user['password'] == password:
        session['username'] = username  # Store username in session
        return redirect(url_for('chat_page'))
    else:
        return "Invalid username or password", 401

# Route to display the sign-up page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Route to handle the sign-up form submission
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    # Check if username is already taken
    if username in users_db:
        return "Username is already taken", 400
    
    # Store the new user data in the in-memory database (users_db)
    users_db[username] = {'password': password, 'email': email}
    
    # Redirect to the login page after successful sign-up
    return redirect(url_for('login_page'))

# Route to display the chat page
@app.route('/chat')
def chat_page():
    # Ensure user is logged in
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    return render_template('index.html', username=session['username'])

# WebSocket route to handle real-time chat
@socketio.on('message')
def handle_message(data):
    emit('message', {'username': session.get('username'), 'message': data}, broadcast=True)

if __name__ == '__main__':
    print("Starting Flask app...")
    socketio.run(app, debug=True)
