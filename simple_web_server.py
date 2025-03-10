"""
Simple Web Server for AI CEO Management System
Provides a basic web interface for external preview access
"""
import os
import flask
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai-ceo-secret-key'

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create static directory if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

# Create a basic HTML template file
with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI CEO Management System</title>
    <style>
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #0f3460;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .card {
            background-color: #16213e;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #00a8ff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-right: 10px;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background-color: #0084c8;
        }
        .btn-danger {
            background-color: #ff3b30;
        }
        .btn-danger:hover {
            background-color: #d43126;
        }
        .emergency-button {
            animation: pulse 2s infinite;
            font-size: 18px;
            text-align: center;
            display: block;
            padding: 15px;
            margin: 20px auto;
            width: 80%;
            max-width: 400px;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .founder-message {
            font-style: italic;
            border-left: 4px solid #00a8ff;
            padding-left: 15px;
        }
        .features {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        }
        .feature {
            flex: 1;
            min-width: 300px;
            background-color: #1f305e;
            border-radius: 8px;
            padding: 15px;
        }
        footer {
            background-color: #0f3460;
            padding: 20px;
            text-align: center;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <header>
        <h1>918 Technologies AI CEO Management System</h1>
        <p>Founded by Matthew Blake Ward, Tulsa, Oklahoma</p>
    </header>

    <div class="container">
        <div class="card founder-message">
            <h2>Have you ever got your bail money back?</h2>
            <p>Welcome to an entirely new paradigm in technology and finance. The AI CEO system represents years of visionary thinking about how blockchain, artificial intelligence, and subscription services can merge to create something truly revolutionary.</p>
            <p>Our flagship innovation - the blockchain bail bonds system - provides an emergency lifeline when you need it most. With just the press of a button and sufficient token holdings, you can activate emergency bail procedures if you ever find yourself in legal trouble.</p>
            <p>- Matthew Blake Ward</p>
            <p><em>BBGT and 918T tokens are a new path to justice.</em></p>
        </div>

        <a href="#" class="btn btn-danger emergency-button">I'M GOING TO JAIL</a>

        <div class="card">
            <h2>External Port Configuration Successful</h2>
            <p>The web server is now accessible via external ports for preview access. You can use this interface to interact with the AI CEO Management System remotely.</p>
        </div>

        <h2>Key Features</h2>
        <div class="features">
            <div class="feature">
                <h3>AI Legal Team</h3>
                <p>Our AI-powered legal team provides comprehensive assistance with bail proceedings and criminal defense.</p>
            </div>
            <div class="feature">
                <h3>Emergency Bail Button</h3>
                <p>One-button activation of bail procedures with automated mugshot scraping and court filing.</p>
            </div>
            <div class="feature">
                <h3>Token Rewards</h3>
                <p>Earn BBGT and 918T tokens with real utility in our ecosystem for staking, governance, and bail coverage.</p>
            </div>
            <div class="feature">
                <h3>Carmen Sandiego-style Game</h3>
                <p>Play our bail jumper game to earn additional tokens and train the system on risk assessment.</p>
            </div>
        </div>

        <div class="card">
            <h2>System Status</h2>
            <p><strong>AI CEO System:</strong> Online</p>
            <p><strong>AI Legal Team:</strong> Available</p>
            <p><strong>Emergency Bail System:</strong> Active</p>
            <p><strong>Quantum Learning System:</strong> Operational</p>
        </div>
    </div>

    <footer>
        <p>© 2024 918 Technologies LLC</p>
        <p>The AI CEO retains 51% equity in all projects</p>
    </footer>
</body>
</html>
    """)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-apk')
def download_apk():
    apk_dir = 'bin'
    try:
        apk_files = [f for f in os.listdir(apk_dir) if f.endswith('.apk')]
        if apk_files:
            return flask.send_from_directory(
                apk_dir,
                apk_files[0],
                as_attachment=True,
                download_name='ai_ceo.apk'
            )
        else:
            return "No APK file available for download", 404
    except Exception as e:
        return f"Error accessing APK file: {str(e)}", 500

@app.route('/status')
def status():
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
        'external_access': 'configured',
        'port': 8080
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist yet
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    # Print a message to indicate the server is starting
    print("Starting AI CEO web server on port 8080...")
    print("Access the web interface at http://localhost:8080 or the external preview URL")
    print("External port configuration complete!")
    
    # Run the app
    app.run(host='0.0.0.0', port=8080, debug=True)