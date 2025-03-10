"""
AI CEO Management System - Simple Web Preview
A dedicated web server that works with Replit's webview
"""
from flask import Flask, render_template, jsonify, redirect, url_for, request, session
import os
import json
import time
import uuid

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)  # For session management

# In-memory storage for demo purposes
users = {
    "demo@example.com": {
        "password": "password123",
        "name": "John Doe",
        "tokens": {
            "BBGT": 500,
            "918T": 20
        },
        "subscription": {
            "type": "Premium",
            "status": "Trial",
            "expires_at": time.time() + 10800  # 3 hours from now
        }
    }
}

founders = {
    "matthew@918technologies.com": {
        "password": "founder123",
        "name": "Matthew Blake Ward",
        "role": "Founder & CEO"
    }
}

@app.route('/')
def index():
    """Display the home page"""
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if it's a founder login
        if email in founders and founders[email]['password'] == password:
            session['user_id'] = email
            session['is_founder'] = True
            return redirect(url_for('founder_dashboard'))
            
        # Check regular user login
        if email in users and users[email]['password'] == password:
            session['user_id'] = email
            session['is_founder'] = False
            return redirect(url_for('dashboard'))
            
        # Failed login
        return render_template('login.html', error="Invalid email or password")
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup"""
    if request.method == 'POST':
        # In a real application, we would validate and save the user
        # For demo, just redirect to dashboard
        return redirect(url_for('dashboard'))
        
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Get user info
    user_id = session['user_id']
    if user_id in users:
        return render_template('dashboard.html', user=users[user_id])
    
    # If user not found, redirect to login
    session.clear()
    return redirect(url_for('login'))

@app.route('/founder-dashboard')
def founder_dashboard():
    """Founder dashboard"""
    # Check if user is logged in and is a founder
    if 'user_id' not in session or not session.get('is_founder', False):
        return redirect(url_for('login'))
        
    # Get founder info
    founder_id = session['user_id']
    if founder_id in founders:
        return render_template('founder_dashboard.html', founder=founders[founder_id])
    
    # If founder not found, redirect to login
    session.clear()
    return redirect(url_for('login'))

@app.route('/borg-assimilation')
def borg_assimilation():
    """Borg-themed project creation page"""
    return render_template('borg_assimilation.html')

@app.route('/terminator-bail')
def terminator_bail():
    """Terminator-themed bail bonds and bounty hunting page"""
    return render_template('terminator_bail.html')

@app.route('/emergency')
def emergency():
    """Emergency bail button page - Terminator themed"""
    return render_template('terminator_bail.html')

@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/status')
def status():
    """Return the system status as JSON"""
    return jsonify({
        'status': 'online',
        'system_name': 'AI CEO Management System',
        'founder': 'Matthew Blake Ward',
        'location': 'Tulsa, Oklahoma',
        'features': [
            'AI Legal Team',
            'Emergency Bail Button',
            'Carmen Sandiego-style Game',
            'Token Rewards System'
        ],
        'token_prices': {
            'BBGT': '0.001 ETH',
            '918T': '0.01 ETH'
        },
        'subscription': {
            'base_price': '$49.99/month',
            'trial_period': '3 hours'
        },
        'timestamp': time.time()
    })

@app.route('/process_signup', methods=['POST'])
def process_signup():
    """Handle signup form submission"""
    # In a real app, we would validate the input and store the user information
    return redirect(url_for('dashboard'))

@app.route('/process_project', methods=['POST'])
def process_project():
    """Handle project creation form submission"""
    # In a real app, we would validate the input and store the project information
    return redirect(url_for('dashboard'))

@app.route('/demo-login')
def demo_login():
    """Quick demo login for testing purposes"""
    session['user_id'] = "demo@example.com"
    session['is_founder'] = False
    return redirect(url_for('dashboard'))

@app.route('/founder-demo-login')
def founder_demo_login():
    """Quick demo login for founder testing"""
    session['user_id'] = "matthew@918technologies.com"
    session['is_founder'] = True
    return redirect(url_for('founder_dashboard'))

# Create a simple home.html template in case it doesn't exist
@app.route('/create-templates')
def create_templates():
    """Create basic templates if they don't exist"""
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('templates/home.html'):
        with open('templates/home.html', 'w') as f:
            f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>AI CEO Management System</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #1a1a2e;
                        color: #e6e6e6;
                    }
                    .container {
                        max-width: 1000px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .header {
                        text-align: center;
                        margin-bottom: 30px;
                        border-bottom: 1px solid #00a8ff;
                        padding-bottom: 15px;
                    }
                    .card {
                        background-color: #16213e;
                        border-radius: 10px;
                        margin-bottom: 20px;
                        overflow: hidden;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    }
                    .card-header {
                        background-color: #0f3460;
                        padding: 15px;
                        border-bottom: 1px solid #00a8ff;
                    }
                    .card-body {
                        padding: 20px;
                    }
                    h1, h2, h3 {
                        color: #00a8ff;
                    }
                    .btn {
                        display: inline-block;
                        background-color: #e94560;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                        margin: 5px;
                        border: none;
                        cursor: pointer;
                        font-weight: bold;
                        transition: background-color 0.3s;
                    }
                    .btn:hover {
                        background-color: #c73a54;
                    }
                    .footer {
                        text-align: center;
                        margin-top: 50px;
                        border-top: 1px solid #00a8ff;
                        padding-top: 15px;
                        font-size: 0.8em;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>AI CEO Management System</h1>
                        <p>Founded by Matthew Blake Ward, Tulsa, Oklahoma</p>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <h2>Welcome to AI CEO</h2>
                        </div>
                        <div class="card-body">
                            <p>Please login or sign up to continue.</p>
                            <div style="text-align: center;">
                                <a href="/login" class="btn">Login</a>
                                <a href="/signup" class="btn">Sign Up</a>
                                <a href="/demo-login" class="btn">Demo Mode</a>
                            </div>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>© 2024 918 Technologies LLC - All rights reserved</p>
                    </div>
                </div>
            </body>
            </html>
            """)
    
    if not os.path.exists('templates/login.html'):
        with open('templates/login.html', 'w') as f:
            f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>AI CEO - Login</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #1a1a2e;
                        color: #e6e6e6;
                    }
                    .container {
                        max-width: 500px;
                        margin: 50px auto;
                        padding: 20px;
                    }
                    .card {
                        background-color: #16213e;
                        border-radius: 10px;
                        overflow: hidden;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    }
                    .card-header {
                        background-color: #0f3460;
                        padding: 15px;
                        text-align: center;
                        border-bottom: 1px solid #00a8ff;
                    }
                    .card-body {
                        padding: 20px;
                    }
                    h1, h2, h3 {
                        color: #00a8ff;
                        margin-top: 0;
                    }
                    .form-group {
                        margin-bottom: 15px;
                    }
                    label {
                        display: block;
                        margin-bottom: 5px;
                    }
                    input[type="email"],
                    input[type="password"] {
                        width: 100%;
                        padding: 10px;
                        border: 1px solid #00a8ff;
                        border-radius: 5px;
                        background-color: #0d1b2a;
                        color: #e6e6e6;
                    }
                    .btn {
                        display: inline-block;
                        background-color: #e94560;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                        margin: 5px 0;
                        border: none;
                        cursor: pointer;
                        font-weight: bold;
                        transition: background-color 0.3s;
                        width: 100%;
                    }
                    .btn:hover {
                        background-color: #c73a54;
                    }
                    .error {
                        color: #ff6b6b;
                        margin-bottom: 15px;
                    }
                    .back-link {
                        text-align: center;
                        margin-top: 20px;
                    }
                    .back-link a {
                        color: #00a8ff;
                        text-decoration: none;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="card">
                        <div class="card-header">
                            <h2>Login to AI CEO</h2>
                        </div>
                        <div class="card-body">
                            {% if error %}
                            <div class="error">
                                {{ error }}
                            </div>
                            {% endif %}
                            
                            <form method="post" action="/login">
                                <div class="form-group">
                                    <label for="email">Email</label>
                                    <input type="email" id="email" name="email" required>
                                </div>
                                
                                <div class="form-group">
                                    <label for="password">Password</label>
                                    <input type="password" id="password" name="password" required>
                                </div>
                                
                                <button type="submit" class="btn">Login</button>
                            </form>
                            
                            <div style="text-align: center; margin-top: 20px;">
                                <p>Don't have an account? <a href="/signup" style="color: #00a8ff;">Sign up</a></p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="back-link">
                        <a href="/">← Back to Home</a>
                    </div>
                </div>
            </body>
            </html>
            """)
    
    return "Templates created successfully."

if __name__ == '__main__':
    # Run the application on port 5000, which is the Replit standard
    print("Starting AI CEO Web Preview on port 5000...")
    
    # Make sure template directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    # Make sure static/images directory exists
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
        
    app.run(host='0.0.0.0', port=5000)